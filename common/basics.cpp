

#include "basics.h"

namespace artDisplay {

pthread_mutex_t debugMutex = PTHREAD_MUTEX_INITIALIZER;
#ifdef USE_FILE_DEBUG
    std::ofstream outl("artDisplay.txt");
#endif
}
