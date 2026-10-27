#include "neo6m.h"

#include <limits.h>
#include <stddef.h>
#include <string.h>

#define NEO6M_SENTENCE_CAPACITY 96U
#define NEO6M_QUEUE_CAPACITY    4U
#define NEO6M_MAX_FIELDS        15U

typedef struct
{
  char text[NEO6M_SENTENCE_CAPACITY];
  uint32_t received_ms;
} NEO6M_QueuedSentence;

static UART_HandleTypeDef *gps_uart;
static uint8_t rx_byte;
static char assembly_buffer[NEO6M_SENTENCE_CAPACITY];
static uint16_t assembly_length;
static bool assembling_sentence;
static NEO6M_QueuedSentence sentence_queue[NEO6M_QUEUE_CAPACITY];
static volatile uint8_t queue_head;
static volatile uint8_t queue_tail;
static volatile bool uart_activity_seen;
static volatile bool receive_rearm_required;
static volatile uint32_t last_uart_rx_ms;
static NEO6M_Data latest_data;

static bool sentence_type_is_supported(const char *sentence,
                                       uint16_t length)
{
  if ((sentence == NULL) || (length < 7U) || (sentence[0] != '$'))
  {
    return false;
  }

  if (!(((sentence[1] == 'G') && (sentence[2] == 'P')) ||
        ((sentence[1] == 'G') && (sentence[2] == 'N'))))
  {
    return false;
  }

  return (sentence[3] == 'G') && (sentence[4] == 'G') &&
         (sentence[5] == 'A') && (sentence[6] == ',');
}

static void queue_completed_sentence(void)
{
  const uint8_t next_head =
      (uint8_t)((queue_head + 1U) % NEO6M_QUEUE_CAPACITY);

  if (!sentence_type_is_supported(assembly_buffer, assembly_length) ||
      (next_head == queue_tail))
  {
    return;
  }

  memcpy(sentence_queue[queue_head].text, assembly_buffer,
         (size_t)assembly_length + 1U);
  sentence_queue[queue_head].received_ms = HAL_GetTick();
  __DMB();
  queue_head = next_head;
}

static void consume_received_byte(uint8_t byte)
{
  if (byte == (uint8_t)'$')
  {
    assembly_length = 0U;
    assembly_buffer[assembly_length++] = (char)byte;
    assembling_sentence = true;
    return;
  }

  if (!assembling_sentence)
  {
    return;
  }

  if (byte == (uint8_t)'\n')
  {
    assembly_buffer[assembly_length] = '\0';
    queue_completed_sentence();
    assembling_sentence = false;
    assembly_length = 0U;
    return;
  }

  if (byte == (uint8_t)'\r')
  {
    return;
  }

  if (assembly_length >= (NEO6M_SENTENCE_CAPACITY - 1U))
  {
    assembling_sentence = false;
    assembly_length = 0U;
    return;
  }

  assembly_buffer[assembly_length++] = (char)byte;
}

static int8_t hexadecimal_value(char character)
{
  if ((character >= '0') && (character <= '9'))
  {
    return (int8_t)(character - '0');
  }
  if ((character >= 'A') && (character <= 'F'))
  {
    return (int8_t)(character - 'A' + 10);
  }
  if ((character >= 'a') && (character <= 'f'))
  {
    return (int8_t)(character - 'a' + 10);
  }
  return -1;
}

static bool checksum_is_valid(char *sentence, char **checksum_marker)
{
  char *cursor;
  char *marker;
  uint8_t calculated = 0U;
  int8_t high_nibble;
  int8_t low_nibble;

  if ((sentence == NULL) || (sentence[0] != '$'))
  {
    return false;
  }

  marker = strchr(sentence, '*');
  if ((marker == NULL) || (marker[1] == '\0') || (marker[2] == '\0') ||
      (marker[3] != '\0'))
  {
    return false;
  }

  for (cursor = &sentence[1]; cursor < marker; ++cursor)
  {
    calculated ^= (uint8_t)*cursor;
  }

  high_nibble = hexadecimal_value(marker[1]);
  low_nibble = hexadecimal_value(marker[2]);
  if ((high_nibble < 0) || (low_nibble < 0) ||
      (calculated != (uint8_t)(((uint8_t)high_nibble << 4) |
                              (uint8_t)low_nibble)))
  {
    return false;
  }

  if (checksum_marker != NULL)
  {
    *checksum_marker = marker;
  }
  return true;
}

static bool parse_unsigned(const char *text, uint32_t maximum,
                           uint32_t *value)
{
  uint32_t result = 0U;

  if ((text == NULL) || (value == NULL) || (*text == '\0'))
  {
    return false;
  }

  while (*text != '\0')
  {
    uint32_t digit;
    if ((*text < '0') || (*text > '9'))
    {
      return false;
    }
    digit = (uint32_t)(*text - '0');
    if ((digit > maximum) || (result > ((maximum - digit) / 10U)))
    {
      return false;
    }
    result = result * 10U + digit;
    ++text;
  }

  *value = result;
  return true;
}

static bool parse_utc(const char *text, uint8_t *hours, uint8_t *minutes,
                      uint8_t *seconds)
{
  uint32_t parsed_hours;
  uint32_t parsed_minutes;
  uint32_t parsed_seconds;

  if ((text == NULL) || (hours == NULL) || (minutes == NULL) ||
      (seconds == NULL) || (strlen(text) < 6U))
  {
    return false;
  }

  if ((text[0] < '0') || (text[0] > '9') ||
      (text[1] < '0') || (text[1] > '9') ||
      (text[2] < '0') || (text[2] > '9') ||
      (text[3] < '0') || (text[3] > '9') ||
      (text[4] < '0') || (text[4] > '9') ||
      (text[5] < '0') || (text[5] > '9') ||
      ((text[6] != '\0') && (text[6] != '.')))
  {
    return false;
  }

  parsed_hours = (uint32_t)(text[0] - '0') * 10U +
                 (uint32_t)(text[1] - '0');
  parsed_minutes = (uint32_t)(text[2] - '0') * 10U +
                   (uint32_t)(text[3] - '0');
  parsed_seconds = (uint32_t)(text[4] - '0') * 10U +
                   (uint32_t)(text[5] - '0');
  if ((parsed_hours > 23U) || (parsed_minutes > 59U) ||
      (parsed_seconds > 59U))
  {
    return false;
  }

  if (text[6] == '.')
  {
    const char *fraction = &text[7];
    if (*fraction == '\0')
    {
      return false;
    }
    while (*fraction != '\0')
    {
      if ((*fraction < '0') || (*fraction > '9'))
      {
        return false;
      }
      ++fraction;
    }
  }

  *hours = (uint8_t)parsed_hours;
  *minutes = (uint8_t)parsed_minutes;
  *seconds = (uint8_t)parsed_seconds;
  return true;
}

static bool parse_coordinate(const char *text, char hemisphere,
                             bool latitude, int32_t *degrees_e7)
{
  const char *decimal_point;
  size_t whole_digits;
  size_t degree_digits;
  uint32_t degrees = 0U;
  uint32_t whole_minutes;
  uint32_t fractional_minutes = 0U;
  uint32_t fractional_scale = 1U;
  uint32_t fraction_digits = 0U;
  int64_t result;
  const char *cursor;

  if ((text == NULL) || (degrees_e7 == NULL) || (*text == '\0'))
  {
    return false;
  }

  decimal_point = strchr(text, '.');
  whole_digits = (decimal_point != NULL) ?
                 (size_t)(decimal_point - text) : strlen(text);
  degree_digits = latitude ? 2U : 3U;
  if (whole_digits != (degree_digits + 2U))
  {
    return false;
  }

  for (cursor = text; cursor < &text[degree_digits]; ++cursor)
  {
    if ((*cursor < '0') || (*cursor > '9'))
    {
      return false;
    }
    degrees = degrees * 10U + (uint32_t)(*cursor - '0');
  }

  if ((text[degree_digits] < '0') || (text[degree_digits] > '9') ||
      (text[degree_digits + 1U] < '0') ||
      (text[degree_digits + 1U] > '9'))
  {
    return false;
  }
  whole_minutes = (uint32_t)(text[degree_digits] - '0') * 10U +
                  (uint32_t)(text[degree_digits + 1U] - '0');

  if (decimal_point != NULL)
  {
    cursor = decimal_point + 1;
    if (*cursor == '\0')
    {
      return false;
    }
    while (*cursor != '\0')
    {
      if ((*cursor < '0') || (*cursor > '9'))
      {
        return false;
      }
      if (fraction_digits < 7U)
      {
        fractional_minutes = fractional_minutes * 10U +
                             (uint32_t)(*cursor - '0');
        fractional_scale *= 10U;
        ++fraction_digits;
      }
      ++cursor;
    }
  }

  if ((whole_minutes >= 60U) ||
      (latitude && (degrees > 90U)) ||
      (!latitude && (degrees > 180U)) ||
      (((latitude && (degrees == 90U)) ||
        (!latitude && (degrees == 180U))) &&
       ((whole_minutes != 0U) || (fractional_minutes != 0U))))
  {
    return false;
  }

  result = (int64_t)degrees * 10000000LL;
  result += (((int64_t)whole_minutes * 10000000LL) +
             (((int64_t)fractional_minutes * 10000000LL) /
              (int64_t)fractional_scale) + 30LL) / 60LL;

  if ((hemisphere == 'S') || (hemisphere == 'W'))
  {
    result = -result;
  }
  else if (!((latitude && (hemisphere == 'N')) ||
             (!latitude && (hemisphere == 'E'))))
  {
    return false;
  }

  if ((result < INT32_MIN) || (result > INT32_MAX))
  {
    return false;
  }
  *degrees_e7 = (int32_t)result;
  return true;
}

static bool parse_altitude_mm(const char *text, int32_t *altitude_mm)
{
  bool negative = false;
  int64_t whole = 0;
  uint32_t fraction = 0U;
  uint32_t fraction_digits = 0U;
  const char *cursor = text;
  int64_t result;

  if ((text == NULL) || (altitude_mm == NULL) || (*text == '\0'))
  {
    return false;
  }

  if ((*cursor == '-') || (*cursor == '+'))
  {
    negative = (*cursor == '-');
    ++cursor;
  }
  if ((*cursor < '0') || (*cursor > '9'))
  {
    return false;
  }

  while ((*cursor >= '0') && (*cursor <= '9'))
  {
    if (whole > 100000L)
    {
      return false;
    }
    whole = whole * 10L + (int64_t)(*cursor - '0');
    ++cursor;
  }

  if (*cursor == '.')
  {
    ++cursor;
    if ((*cursor < '0') || (*cursor > '9'))
    {
      return false;
    }
    while ((*cursor >= '0') && (*cursor <= '9'))
    {
      if (fraction_digits < 3U)
      {
        fraction = fraction * 10U + (uint32_t)(*cursor - '0');
        ++fraction_digits;
      }
      ++cursor;
    }
  }
  if (*cursor != '\0')
  {
    return false;
  }

  while (fraction_digits < 3U)
  {
    fraction *= 10U;
    ++fraction_digits;
  }
  result = whole * 1000L + (int64_t)fraction;
  if (negative)
  {
    result = -result;
  }
  if ((result < INT32_MIN) || (result > INT32_MAX))
  {
    return false;
  }

  *altitude_mm = (int32_t)result;
  return true;
}

static bool parse_gga(char *sentence, uint32_t received_ms)
{
  char *fields[NEO6M_MAX_FIELDS];
  char *checksum_marker;
  char *cursor;
  uint8_t field_count = 0U;
  uint32_t fix_quality;
  uint32_t satellites;
  NEO6M_Data parsed = latest_data;

  if (!checksum_is_valid(sentence, &checksum_marker))
  {
    return false;
  }
  *checksum_marker = '\0';

  fields[field_count++] = &sentence[1];
  for (cursor = &sentence[1]; (*cursor != '\0') &&
                              (field_count < NEO6M_MAX_FIELDS); ++cursor)
  {
    if (*cursor == ',')
    {
      *cursor = '\0';
      fields[field_count++] = cursor + 1;
    }
  }

  if ((field_count < 11U) || !parse_unsigned(fields[6], 8U, &fix_quality) ||
      !parse_unsigned(fields[7], UINT8_MAX, &satellites))
  {
    return false;
  }

  parsed.utc_valid = false;
  if (fields[1][0] != '\0')
  {
    if (!parse_utc(fields[1], &parsed.utc_hours, &parsed.utc_minutes,
                   &parsed.utc_seconds))
    {
      return false;
    }
    parsed.utc_valid = true;
  }

  parsed.data_valid = true;
  parsed.fix_valid = (fix_quality > 0U) && (satellites > 0U);
  parsed.satellites = (uint8_t)satellites;
  parsed.last_update_ms = received_ms;

  if (parsed.fix_valid)
  {
    if (!parsed.utc_valid || (strlen(fields[3]) != 1U) ||
        (strlen(fields[5]) != 1U) ||
        !parse_coordinate(fields[2], fields[3][0], true,
                          &parsed.latitude_deg_e7) ||
        !parse_coordinate(fields[4], fields[5][0], false,
                          &parsed.longitude_deg_e7) ||
        !parse_altitude_mm(fields[9], &parsed.altitude_mm) ||
        (strcmp(fields[10], "M") != 0))
    {
      return false;
    }
    parsed.last_fix_ms = received_ms;
  }

  latest_data = parsed;
  return true;
}

HAL_StatusTypeDef NEO6M_Init(UART_HandleTypeDef *uart)
{
  if (uart == NULL)
  {
    return HAL_ERROR;
  }

  gps_uart = uart;
  rx_byte = 0U;
  assembly_length = 0U;
  assembling_sentence = false;
  queue_head = 0U;
  queue_tail = 0U;
  uart_activity_seen = false;
  receive_rearm_required = false;
  last_uart_rx_ms = 0U;
  memset(&latest_data, 0, sizeof(latest_data));
  if (HAL_UART_Receive_IT(gps_uart, &rx_byte, 1U) != HAL_OK)
  {
    receive_rearm_required = true;
    return HAL_ERROR;
  }
  return HAL_OK;
}

void NEO6M_Process(void)
{
  if (receive_rearm_required && (gps_uart != NULL) &&
      (HAL_UART_Receive_IT(gps_uart, &rx_byte, 1U) == HAL_OK))
  {
    receive_rearm_required = false;
  }

  while (queue_tail != queue_head)
  {
    NEO6M_QueuedSentence *sentence = &sentence_queue[queue_tail];
    __DMB();
    (void)parse_gga(sentence->text, sentence->received_ms);
    queue_tail = (uint8_t)((queue_tail + 1U) % NEO6M_QUEUE_CAPACITY);
  }
}

bool NEO6M_GetData(NEO6M_Data *data)
{
  if (data == NULL)
  {
    return false;
  }
  *data = latest_data;
  return latest_data.data_valid;
}

bool NEO6M_IsUartActive(uint32_t now_ms, uint32_t maximum_age_ms)
{
  return uart_activity_seen &&
         ((now_ms - last_uart_rx_ms) <= maximum_age_ms);
}

bool NEO6M_IsDataFresh(const NEO6M_Data *data, uint32_t now_ms,
                       uint32_t maximum_age_ms)
{
  return (data != NULL) && data->data_valid &&
         ((now_ms - data->last_update_ms) <= maximum_age_ms);
}

void NEO6M_UART_RxCpltCallback(UART_HandleTypeDef *uart)
{
  if ((uart == NULL) || (uart != gps_uart))
  {
    return;
  }

  last_uart_rx_ms = HAL_GetTick();
  uart_activity_seen = true;
  consume_received_byte(rx_byte);
  receive_rearm_required =
      (HAL_UART_Receive_IT(gps_uart, &rx_byte, 1U) != HAL_OK);
}

void NEO6M_UART_ErrorCallback(UART_HandleTypeDef *uart)
{
  if ((uart == NULL) || (uart != gps_uart))
  {
    return;
  }

  assembly_length = 0U;
  assembling_sentence = false;
  receive_rearm_required =
      (HAL_UART_Receive_IT(gps_uart, &rx_byte, 1U) != HAL_OK);
}
