/**
 * @ingroup     examples
 * @{
 *
 * @file        udp_rx.h
 * @brief       UDP receiver thread header file
 *
 * @author      Kristina Kaypaghian, Tina Bao
 *
 * Github Link: https://github.com/usc-ee250-fall2018/finalproj-riot-kristtinafinal
 *
 * @}
 */

/* Header files are used to share global functions and variables. */

#include "kernel_types.h"
#include "mutex.h"

typedef struct {
    mutex_t *mutex;
    uint32_t udp_port;
} udp_rx_args_t;

kernel_pid_t udp_rx_init(void *args);

/**
 * @def THREAD_STACKSIZE_DEFAULT
 * @brief A reasonable default stack size that will suffice most smaller tasks
 *
 * @note This value must be defined by the CPU specific implementation, please
 *       take a look at @c cpu/$CPU/include/cpu_conf.h
 */
#ifndef THREAD_STACKSIZE_DEFAULT
//#error THREAD_STACKSIZE_DEFAULT must be defined per CPU
#endif
#ifdef DOXYGEN
#define THREAD_STACKSIZE_DEFAULT      (THREAD_STACKSIZE_MAIN)
#endif

/**
 * @def THREAD_EXTRA_STACKSIZE_PRINTF
 * @brief Size of the task's printf stack in bytes
 *
 * @note This value must be defined by the CPU specific implementation, please
 *       take a look at @c cpu/$CPU/include/cpu_conf.h
 */
#ifndef THREAD_EXTRA_STACKSIZE_PRINTF
//#error THREAD_EXTRA_STACKSIZE_PRINTF must be defined per CPU
#endif
#ifdef DOXYGEN
#define THREAD_EXTRA_STACKSIZE_PRINTF      (THREAD_STACKSIZE_MAIN)
#endif

/**
 * @def THREAD_STACKSIZE_MAIN
 * @brief Size of the main task's stack in bytes
 */
#ifndef THREAD_STACKSIZE_MAIN
#define THREAD_STACKSIZE_MAIN      (THREAD_STACKSIZE_DEFAULT + THREAD_EXTRA_STACKSIZE_PRINTF)
#endif

/**
 * @brief Do not automatically call thread_yield() after creation: the newly
 *        created thread might not run immediately. Purely for optimization.
 *        Any other context switch (i.e. an interrupt) can still start the
 *        thread at any time!
 */
#define THREAD_CREATE_WOUT_YIELD        (4)