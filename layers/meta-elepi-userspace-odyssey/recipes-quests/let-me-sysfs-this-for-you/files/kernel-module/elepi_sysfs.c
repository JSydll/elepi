/*
elepi_sysfs.c

Implements a small kernel module that populates a sysfs entry
with a structure resembling a device driver or similar.

*/
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/kobject.h>
#include <linux/module.h>
#include <linux/sysfs.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Joschka Seydell");
MODULE_DESCRIPTION("Allows to query elePi solution code fragments over an sysfs interface.");
MODULE_VERSION("1.0");

#define SYSFS_PARENT_ENTRY "elepi"

static struct kobject *this_module;

// User-relevant data
// 

typedef enum {
    FIRST = 0,
    SECOND = 1,
    INVALID = 2,
    UNDEFINED = 3,
} fragment_choice;

static const char *fragment_choice_names[] = {
    "first", "second", "invalid selection", "undefined"
};
static const char *fragment_values[] = {
    "aef7803de139ec28d9aa20d3281fa439a809617500b3d8d85b7a3bea44d13c67", 
    "de6bc49fefd7d0bac331d10c0e216124247f835d640d58735b4d047d3ab93b2c"};
static fragment_choice selected = UNDEFINED;

// Attribute for printing help
//

static ssize_t info_show(struct kobject *kobj,
                         struct kobj_attribute *attr,
                         char *buf)
{
    return sprintf(buf, "This module allows to query elePi solution code fragments.\n"
                        "You first have to 'select' which fragment to display ('first' or 'second'), "
                        "then you can read the 'fragment'.\n");
}

static struct kobj_attribute info_attr = __ATTR_RO(info);

// Attribute for selecting a fragment
//

static ssize_t select_show(struct kobject *kobj,
                                    struct kobj_attribute *attr,
                                    char *buf)
{
    return sprintf(buf, "%s\n", fragment_choice_names[selected]);
}

static ssize_t select_store(struct kobject *kobj,
                                     struct kobj_attribute *attr,
                                     const char *buf,
                                     size_t count)
{
    char input[20];
    sscanf(buf, "%s", input);
    for (int i = 0;i < (int) INVALID;i++)
    {
        if (strcmp(input, fragment_choice_names[i]) == 0)
        {
            selected = (fragment_choice) i;
            return count;
        }
    }
    selected = INVALID;
    return count;
}

static struct kobj_attribute select_attr = __ATTR_RW(select);

// Attribute for displaying fragments
//

static ssize_t fragment_show(struct kobject *kobj,
                             struct kobj_attribute *attr,
                             char *buf)
{
    if (selected > SECOND)
    {
        return sprintf(buf, "%s\n", fragment_choice_names[selected]);
    }
    return sprintf(buf, "%s\n", fragment_values[selected]);
}

static struct kobj_attribute fragment_attr = __ATTR_RO(fragment);


// Module initialization and exit
//

static int __init this_module_init(void) 
{ 
    int error = 0;

    this_module = kobject_create_and_add(SYSFS_PARENT_ENTRY, kernel_kobj);
    if (!this_module)
    {
        return -ENOMEM;
    }

    error = sysfs_create_file(this_module, &info_attr.attr);
    error |= sysfs_create_file(this_module, &select_attr.attr);
    error |= sysfs_create_file(this_module, &fragment_attr.attr);
    if (error)
    { 
        kobject_put(this_module);
        pr_info("Failed to setup the attribute files in /sys/kernel/elepi!\n");
        return error;
    }
    pr_debug("Initialized module - you can query elePi solution code fragments now.\n");
    return 0;
} 

static void __exit this_module_exit(void)
{
    kobject_put(this_module);
    pr_debug("Exited module.\n");
}

module_init(this_module_init);
module_exit(this_module_exit);