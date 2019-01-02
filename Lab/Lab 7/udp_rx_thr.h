/**
 * @ingroup     examples
 * @{
 *
 * @file        udp_rx_thr.h
 * @brief       UDP receiver thread header
 *
 * @author      [Tina Bao & Kristina Kaypaghian]
 *
 * Github Link: [github.com/usc-ee250-fall2018/riot-kristina7]
 *
 * @}
 */

/* Header files are used to share global functions and variables. */

#include "kernel_types.h"

#define UDP_RX_DONE     9 //arbitrary number

typedef struct {
    kernel_pid_t main_pid;
    unsigned int num_pkts;
    uint32_t udp_port;
} udp_rx_args_t;

kernel_pid_t udp_rx_thr_init(void *args);


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