/**
 * @ingroup     examples
 * @{
 *
 * @file        udp_rx_thr.c
 * @brief       UDP receiver thread
 *
 * @author      [Tina Bao & Kristina Kaypaghian]
 *
 * Github Link: [github.com/usc-ee250-fall2018/riot-kristina7]
 *
 * @}
 */

#include <inttypes.h>
#include <stdio.h>

#include "thread.h"
#include "msg.h"
#include "net/gnrc.h"
#include "udp_rx_thr.h"

#define OPENMOTE_BUILD 0
#if OPENMOTE_BUILD
  #include "cc2538_rf.h"
#endif

#define ENABLE_DEBUG (1)
#include "debug.h"

#include "net/gnrc/pkt.h"



/**
 * TODO (Lab 08): implement this functino for the RSS and PRR lab assignment
 *
 * For each packet you receive, you need to extract the Received Signal Strength
 * Indicator (RSSI) from the layer 2 header. The Received Signal Strength (no I)
 * is equal to the RSSI minus CC2538_RSSI_OFFSET. You must cast the original 
 * RSSI value because it is a 2-complement number. This function should 
 * ultimately print out the RSS of the packet inputted.
 */
static void print_rss(gnrc_pktsnip_t *pkt)
{
    //find gnrc_pktsnip_t of type GNRC_NETTYPE_NETIF, data points to 
    //header in format of the struct gnrc_netif_hdr_t
    //cast pointer to type (below)
    gnrc_pktsnip_t *snipheader = gnrc_pktsnip_search_type(pkt, GNRC_NETTYPE_NETIF);
    gnrc_netif_hdr_t *header = snipheader->data;
    int rssi = (int)(header->rssi);
    rssi = rssi - 73;
    printf("%d", rssi);
}

/**
 * TODO (Lab 08): implement this function for the RSS and PRR lab assignment
 *
 * You know the number of packets you need to receive, and how many packets
 * you actually received. Calculate the Packet Reception Ratio and print it
 * out.
 */
static void print_prr(uint32_t pkt_rcv, uint32_t num_pkts)
{
    float prr = (float)pkt_rcv/(float)num_pkts;
    printf("%f\n", prr);
}

/**
 * TODO: implement this function 
 * 
 * When a packet is received, GNRC will give you the packet as a linked list
 * of snips. Look for the snip of type GNRC_NETTYPE_UNDEF. The data here is
 * the packet's payload. Print the payload. You can assume they are readable
 * ascii characters but you can NOT assume the payload is a null terminated
 * string. Thus, you should print based on the size of the data. FYI, this
 * linked list is not circular. You can us gnrc_pktsnip_search_type().
 */
static void _print_payload(gnrc_pktsnip_t *pkt)
{
    gnrc_pktsnip_t *payload = gnrc_pktsnip_search_type(pkt, GNRC_NETTYPE_UNDEF);
    unsigned char i;
    size_t psize = payload->size;
    char* pdata = payload->data;
    for (i = 0; i < psize; i++) {
      printf("%c", pdata[i]);
    }
    //printf("%c", '\0');
}

#define MAIN_QUEUE_SIZE     (8)
char rcv_thread_stack[THREAD_STACKSIZE_MAIN]; 
#define PKT_INTERVAL_USEC   (1000000)
char* troj = "Go Trojans!";

static void *_udp_rx_thr(void *arg)
{
    udp_rx_args_t *udp_rx_args = (udp_rx_args_t *)arg; //cast it to the right type to parse
    kernel_pid_t main_pid = udp_rx_args->main_pid;
    int num_pkts = udp_rx_args->num_pkts;
    uint32_t udp_port = udp_rx_args->udp_port;


    msg_t msg, reply;

    reply.content.value = (uint32_t)(-ENOTSUP);     
    reply.type = GNRC_NETAPI_MSG_TYPE_ACK; 

    //TODO: what is `msg_t reply` used for? see the documentation in gnrc.h. 
    //This is a weird quirk of the RIOT-OS kernel design, so we have to include it.


    int rcvd_all_pkts = 0;


    static msg_t msg_queue[MAIN_QUEUE_SIZE];

    /* setup the message queue */
    msg_init_queue(msg_queue, sizeof(msg_queue));


    /* TODO: create and init this thread's msg queue for async messages */
    /* TODO: register this thread to UDP packets coming in on udp_port */

    gnrc_netreg_entry_t me_reg = { .demux_ctx = udp_port, .target.pid = thread_getpid() };
    gnrc_netreg_register(GNRC_NETTYPE_UDP, &me_reg);
    

    gnrc_pktsnip_t *pkt = NULL;    

    int num_rcvd = 0; 
    int miss = 0; 
    char start = 0;        

    while (!rcvd_all_pkts) {

        if(num_rcvd == 0) {
            msg_receive(&msg);
            pkt = msg.content.ptr;
            unsigned char c;
            char* pdata = pkt->data; 
                for(c = 0; c <= 10 ; c++) {
                    if (pdata[c] == troj[c]) {
                        start = 1;
                    }
                }
            
        }
        else {
            if (start == 1) {
                if (xtimer_msg_receive_timeout(&msg, (uint32_t)((float)PKT_INTERVAL_USEC*1.1)) < 0) {
                    DEBUG("udp_rx_thr:missed packet number %d!\n", miss);
                    miss++;
                    //add more loop control logic here
                }
            }
        }
        if (start == 1) {
            num_rcvd++;
            //num_pkts--;
            if(num_rcvd == num_pkts) 
                rcvd_all_pkts = 1;
        }

        switch (msg.type) {
            case GNRC_NETAPI_MSG_TYPE_RCV:
                DEBUG("udp_rx_thr: data received: ");
                pkt = msg.content.ptr;
                //_handle_incoming_pkt(pkt);
                _print_payload(pkt);
                printf("\n");

                unsigned char c;
                char flag = 0;
                char* pdata = pkt->data; 
                for(c = 0; c <= 10 ; c++) {
                    if (pdata[c] != troj[c]) {
                        flag = 1;
                    }
                }
                
                print_rss(pkt);
                printf("\n");

                gnrc_pktbuf_release(pkt);
                
                if (flag == 1) {
                    miss++;
                    printf("miss\n");
                    flag = 0;
                    break;
                }

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
                DEBUG("udp: received unidentified message\n");
                break;
        }
    }

    //printf("%d     %d\n", num_rcvd, miss);
    print_prr((num_rcvd - miss), num_rcvd);


    /* TODO: exit the while loop when num_pkts packets have been received */
        /* Use gnrc_pktdump.c as a model and refer to gnrc.h for documentation 
           on how to structure this thread. If you receive a pointer to a packet
           make sure to gnrc_pktbuf_release(msg.content.ptr) to free up space!
           This is not explicitly stated in gnrc.h but you can see how it's
           done in gnrc_pktdump.c. */


    /* TODO: Unregister this thread from UDP packets. Technically unnecessary, 
    but let's do it for completion and good practice. */

    gnrc_netreg_unregister(GNRC_NETTYPE_UDP, &me_reg);

    /* send shutdown message to main thread */
    
    msg.type = UDP_RX_DONE;
    msg.content.value = 0; //we are not using this field
    msg_send(&msg, main_pid);

    return 0;
}

kernel_pid_t udp_rx_thr_init(void *args)
{
    kernel_pid_t pid = thread_create(rcv_thread_stack , sizeof(rcv_thread_stack), THREAD_PRIORITY_MAIN,
                                        THREAD_CREATE_STACKTEST,
                                        _udp_rx_thr, args, "udp_rx_thr");


    return pid;

    /* What is `args` supposed to be?!
      C coders use a pointer to void to tell programmers that this pointer 
      argument can point to anything you need. It could be a pointer to
      a function, variable, struct, etc. This allows for code *flexibility*. 
      When this is called in main(), we cast a pointer to udp_rx_args to (void *) 
      because we know what this pointer actually points to since udp_rx_args_t is 
      a type specific to udp_rx_thr.c/.h. That is, if you are calling 
      udp_rx_thr_init(), you have already read this file which tells shows you
      what will happen to the input argument `args`. 
    */ 

    /* use thread_create() here */
}