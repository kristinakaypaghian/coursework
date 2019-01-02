/**
 * @ingroup     examples
 * @{
 *
 * @file        udp_rx.c
 * @brief       UDP receiver thread
 *
 * @author      Kristina Kaypaghian, Tina Bao
 *
 * Github Link: https://github.com/usc-ee250-fall2018/finalproj-riot-kristtinafinal
 *
 * @}
 */

#include <inttypes.h>
#include <stdio.h>

#include "thread.h"
#include "msg.h"
#include "net/gnrc.h"
#include "udp_rx.h"
#include "timex.h"
#include "mutex.h"
#include "random.h"

#define ENABLE_DEBUG (1)
#include "debug.h"

#define PRNG_INITVAL            100
#define SLEEP_MSG_STR           "sleep"
#define SLEEP_MSG_LEN           5

#define SLEEP_INTERVAL_SECS     (4000000)
#define RAND_USLEEP_MIN         (0)
#define RAND_USLEEP_MAX         (1000000)

#define MAIN_QUEUE_SIZE     (8)
char rcv_thread_stack[THREAD_STACKSIZE_MAIN]; 

static void _print_payload(gnrc_pktsnip_t *pkt)
{
    gnrc_pktsnip_t *payload = gnrc_pktsnip_search_type(pkt, GNRC_NETTYPE_UNDEF);
    unsigned char i;
    size_t psize = payload->size;
    char* pdata = payload->data;
    for (i = 0; i < psize; i++) {
      printf("%c", pdata[i]);
    }
}

static void *_udp_rx(void *arg)
{
    udp_rx_args_t *udp_rx_args = (udp_rx_args_t *)arg;
    mutex_t *mutex = udp_rx_args->mutex;
    uint32_t udp_port = udp_rx_args->udp_port;

    msg_t msg, reply;
    reply.content.value = (uint32_t)(-ENOTSUP);     
    reply.type = GNRC_NETAPI_MSG_TYPE_ACK; 

    /* initialize PRNG */
    random_init(PRNG_INITVAL);
    printf("PRNG initialized to current time: %d\n", PRNG_INITVAL);

    static msg_t msg_queue[MAIN_QUEUE_SIZE];

    /* setup the message queue */
    msg_init_queue(msg_queue, sizeof(msg_queue));

    gnrc_netreg_entry_t me_reg = { .demux_ctx = udp_port, .target.pid = thread_getpid() };
    gnrc_netreg_register(GNRC_NETTYPE_UDP, &me_reg);

    while (1) {
        msg_receive(&msg);
        gnrc_pktsnip_t *pkt = NULL;
        pkt = msg.content.ptr; // payload

        //_handle_incoming_pkt(pkt);
        _print_payload(pkt);
        printf("\n");

        unsigned char c;
        char flag = 0;
        char* pdata = pkt->data; 
        for(c = 0; c <= SLEEP_MSG_LEN ; c++) {
            if (pdata[c] != SLEEP_MSG_STR[c]) {
                flag = 1;
            }
        }

        switch (msg.type) {
            case GNRC_NETAPI_MSG_TYPE_RCV:
                DEBUG("udp_rx: data received\n");

                pkt = msg.content.ptr;
                if (flag != 1) // if(msg size is valid and msg includes sleep string)
                {
                    
                    //LOCK
                    mutex_lock(mutex);
                    printf("Start sleep");

                    /* additional random sleep to reduce network collisions */
                    uint32_t interval = random_uint32_range(RAND_USLEEP_MIN, RAND_USLEEP_MAX);
                    xtimer_usleep(SLEEP_INTERVAL_SECS+interval); // sleep for 4 seconds + random sleep interval
                    
                    //UNLOCK
                    mutex_unlock(mutex);
                    float sleep_total = (SLEEP_INTERVAL_SECS+interval)/1000000;
                    printf("Start sleep. Slept for %d seconds.", (int)sleep_total);

                    //print start, stop, length of sleep

                }


                
                gnrc_pktbuf_release(msg.content.ptr);
                break;

            case GNRC_NETAPI_MSG_TYPE_SND:
                pkt = msg.content.ptr;
                _print_payload(pkt);
                gnrc_pktbuf_release(pkt);
                //_handle_outgoing_pkt(pkt);
                break;
            case GNRC_NETAPI_MSG_TYPE_SET:
            case GNRC_NETAPI_MSG_TYPE_GET:
                msg_reply(&msg, &reply);
                break;


            default:
                DEBUG("udp_rx_thr: received something unexpected");
                break;
        }
    }

    /* should never be reached */
    DEBUG("ERROR!\n");
    return 0;
}

kernel_pid_t udp_rx_init(void *args)
{
    
    kernel_pid_t udp_rx_pid = thread_create(rcv_thread_stack , sizeof(rcv_thread_stack), THREAD_PRIORITY_MAIN,
                                        THREAD_CREATE_STACKTEST,
                                        _udp_rx, args, "udp_rx");
    
    return udp_rx_pid;
}