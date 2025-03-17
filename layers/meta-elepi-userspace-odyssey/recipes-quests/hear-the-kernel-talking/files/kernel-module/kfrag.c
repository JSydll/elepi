/*
kfrag.c

Implements a small kernel module that issues log messages containing
elePi solution code fragments when waken up by writing 'wake' to the
spawned /proc/kfrag_queue file handle.

*/
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/kthread.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/sched.h>
#include <linux/uaccess.h>
#include <linux/wait.h>

MODULE_LICENSE("MIT");
MODULE_AUTHOR("Joschka Seydell");
MODULE_DESCRIPTION("Provides elePi solution code fragments when read or awaken via /proc/kfragments.");
MODULE_VERSION("1.0");

#define PROC_HANDLE "kfragments"

// User-relevant data
// 
static const char *readable_fragment = "a62ca2ad68a1a67a61af0da55ea524f3";
static const char *pollable_fragments[3] = {
    "28006ef60c7b3047240694be412ed22a", 
    "cbcb9c44b6f7e655229182fde1cf3247", 
    "6e2199a0480a8ee4d7e255eb39857965"};
static int current_fragment = 0;

// Multithreading setup
//

static DECLARE_WAIT_QUEUE_HEAD(event_queue);
static int event_queue_flag = 0;
static struct task_struct *event_thread;

// Setup of the /proc filehandle to interact with the event loop
//

static ssize_t on_proc_read(struct file *, char __user *buffer, size_t buffer_length, loff_t *offset)
{
    int len = strlen(readable_fragment); 
    ssize_t ret = len; 
    if (*offset >= len || copy_to_user(buffer, readable_fragment, len)) {
        // Something went wrong
        ret = 0; 
    } else { 
        *offset += len; 
    }
    return ret; 
}

static ssize_t on_proc_write(struct file *, const char __user *buffer, size_t buffer_length, loff_t *)
{
    char local_buffer[10];
    if (buffer_length > sizeof(local_buffer) - 1) {
        return -EINVAL;
    }

    if (copy_from_user(local_buffer, buffer, buffer_length)) {
        return -EFAULT;
    }
    local_buffer[buffer_length] = '\0';

    if (strcmp(local_buffer, "wake\n") == 0) {
        event_queue_flag = 1;
        wake_up_interruptible(&event_queue);
    }

    return buffer_length;
}

static const struct proc_ops proc_fops = {
    .proc_read = on_proc_read,
    .proc_write = on_proc_write,
};

// Waiting for and processing events issued through the /proc filehandle
// 

static int process_events(void *)
{   
    while(true) {
        wait_event_interruptible(event_queue, event_queue_flag != 0);
        if (event_queue_flag == 2) {
            return 0;
        }
        pr_info("elePi quest solution code fragment: %s\n", pollable_fragments[current_fragment++]);
        current_fragment %= 3;
        event_queue_flag = 0;
    }
    do_exit(0);
    return 0;
}

// Module initialization and exit
//

static int __init this_module_init(void) {
    proc_create(PROC_HANDLE, 0666, NULL, &proc_fops);
    event_thread = kthread_create(process_events, NULL, "event_loop");
    if (event_thread) {
        wake_up_process(event_thread);
    } else {
        pr_debug("Failed to setup event thread.\n");
    }
    pr_debug("Initialized module - you can request elePi solution code fragments now.\n");
    return 0;
}

static void __exit this_module_exit(void) {
    event_queue_flag = 2;
    wake_up_interruptible(&event_queue);
    remove_proc_entry(PROC_HANDLE, NULL);
    pr_debug("Exited module.\n");
}

module_init(this_module_init);
module_exit(this_module_exit);