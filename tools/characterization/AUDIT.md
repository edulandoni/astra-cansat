# ASTRA static audit (2026-10-30)

Scope: ASTRA-maintained sources under `flight-software/flight_computer/Core`.
Generated STM32 code and vendor HAL/CMSIS sources were not treated as ASTRA
findings. This audit made no Flight Computer source changes.

## Findings

### MEDIUM — valid stationary gyro frames can be rejected

- File: `Core/Src/mpu6500.c:151`
- Function: `MPU6500_ReadRaw`
- Problem: the sanity check rejects a frame whenever all three gyro words are
  `0x0000` (or all are `0xFFFF`). An all-zero gyro vector is a valid possible
  measurement for a stationary sensor; `-1` on every axis is also representable.
- Impact: legitimate samples can be marked as I2C/read failures. Repetition can
  drive health degradation/recovery and creates selection bias in stationary
  characterization data.
- Recommended action: after characterization, replace value-pattern rejection
  with transport/configuration evidence (HAL status, identity/config checks, or
  a policy that cannot exclude valid sensor codes). Do not change it immediately
  on the hardware-validated flight branch without regression testing.

### MEDIUM — GPS receive re-arm flag has a main/ISR lost-update window

- File: `Core/Src/neo6m.c:412`
- Function: `NEO6M_Process` / `NEO6M_UART_RxCpltCallback`
- Problem: main context calls `HAL_UART_Receive_IT` and then writes
  `receive_rearm_required = false`. Once reception is armed, the RX callback can
  run before that store and set the flag back to `true` if its own re-arm fails;
  main can then overwrite it with `false`.
- Impact: a rare timing-dependent UART re-arm failure can leave GPS reception
  stopped without a pending retry.
- Recommended action: make ownership of the re-arm state single-context, or
  protect the arm-and-flag transition with a short critical section/state
  machine; validate with UART fault injection.

### MEDIUM — RTC update is not atomic across time and date

- File: `Core/Src/app.c:154`
- Function: `App_SetMissionRtc`
- Problem: `HAL_RTC_SetTime` can succeed and `HAL_RTC_SetDate` then fail. The
  backup marker remains cleared, but the peripheral is left partially updated.
- Impact: callers correctly see failure, yet later reads before a successful
  retry can observe a mixed date/time state.
- Recommended action: stage/restore the prior RTC value or explicitly define and
  enforce an invalid-state read policy around a failed two-step update.

### LOW — I2C deinitialization failure is ignored before GPIO recovery

- File: `Core/Src/i2c_bus_manager.c:141`
- Function: `RecoverBus`
- Problem: the return value of `HAL_I2C_DeInit` is discarded before pins are
  repurposed for bus recovery.
- Impact: if deinitialization fails, GPIO clock-pulse recovery proceeds with
  uncertain peripheral/pin state, which can obscure the original failure.
- Recommended action: record the failure and choose an explicit safe fallback;
  retain the current behavior until recovery-path hardware tests exist.

### INFO — dashboard has the largest measured ASTRA stack frame

- File: `Core/Src/debug_console.c:195`
- Function: `DebugConsole_ShowDashboard`
- Problem: GCC `-fstack-usage` reports a 336-byte static frame; its formatting
  helper reports 96 bytes. No unbounded local allocation was found.
- Impact: acceptable against the current 128 KiB RAM budget, but it is the first
  ASTRA frame to re-check if interrupt nesting or stack allocation changes.
- Recommended action: keep stack-usage artifacts in build review; no immediate
  change.

## Reviewed categories with no additional actionable finding

Internal linkage, const use, global state, large stack buffers, formatting and
truncation, integer bounds, signed/unsigned conversions, blocking loops/delays,
stale-data handling, health transitions, duplicate state, and dead code were
reviewed. Existing `snprintf` calls are capacity-bounded. Scheduler and freshness
arithmetic consistently use unsigned subtraction for tick wrap. The short
DS18B20 timing loops and I2C recovery delays are deliberate hardware protocols.
