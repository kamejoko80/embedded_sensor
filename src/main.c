#define TOP_OF_STACK 0x20000800

static void nmi_handler(void);
static void hf_handler(void);
int main(void);

// Set up the vector table
unsigned int *vec_table[4] __attribute__ ((section("vectors"))) = {
    (unsigned int*) TOP_OF_STACK,       // The stack pointer
    (unsigned int*) main,               // Entry point
    (unsigned int*) nmi_handler,        // NMI Handler
    (unsigned int*) hf_handler,         // The hard fault handler
};

int main(void)
{
    int i = 0;
    int j = 1;
    for(;;)
    {
        i++;
        j++;
    }
}

void nmi_handler(void)
{
    for(;;);
}

void hf_handler(void)
{
    for(;;);
}

