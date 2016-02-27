#ifndef BASICS_H_
#define BASICS_H_

#include <iostream>
#include <sstream>
#include <string>
#include <fstream>


//------------------------------------------------------------------
// convenience macros for output
//------------------------------------------------------------------
#ifdef USE_FILE_DEBUG
namespace artDisplay {
extern std::ofstream outl;
#define OUTL(msg) \
    do { \
        artDisplay::outl << msg << std::endl; \
    } while (0)
}
#else
// single line to stderr
#define OUTL(msg) \
    do { \
        std::cerr << msg << std::endl; \
    } while (0)
#endif
// dump and label
#define DUMP(exp) " " << #exp << ":" << (exp)
// dump in hex and label
#define HDUMP(exp) " " << #exp << ":" << std::showbase \
            << std::hex << (exp) << std::dec << std::noshowbase

#define USAGE(exp) \
    do { \
        OUTL("ERROR: " << exp); \
        usage(); \
    } while (0)



//------------------------------------------------------------------
// tests
// - code under test should use ASSERT; this is a lot like standard 
//   assert(), but has a hook that allows tests to verify that an
//   assertion gets hit without terminating the program.
// - tests should generally use the CONFIRM macro to verify behavior;
//   this currently just asserts, but may do more later
// - tests can use CONFIRM_ASSERT to verify that an assertion is hit.
//   (the first parameter is an expression to execute; the second is
//   a substring of the expected assertion; a null or empty substring
//   accepts any assertion)
//------------------------------------------------------------------
extern void Fail();
namespace artDisplay {
    extern pthread_mutex_t debugMutex;
}

#define CODE_LOC " at line " << __LINE__ << ", " << __FILE__

#define FAIL(msg) \
    do { \
        std::stringstream tmp; \
        tmp << msg << CODE_LOC; \
        pthread_mutex_lock(&artDisplay::debugMutex) ; \
        OUTL("****** FATAL ERROR ******"); \
        OUTL(tmp.str()); \
        OUTL("*************************"); \
        pthread_mutex_unlock(&artDisplay::debugMutex) ; \
        throw(tmp.str()); \
    } while (0)

//! a replacement for the standard assert()
//
//! This macro is meant to be used as a replacement for libc assert() to
//! simplify testing.  Where the standard assert() forces the program to exit,
//! this version allows a test program to verify that an assertion
//! failed, and then continue doing further testing.  This is done by
//! setting the global bool ThrowOnFailure to true, and then catching the
//! exception that gets thrown when the assertion fails.  The CONFIRM_ASSERT
//! macro performs this bookkeeping.  A test program should use CONFIRM
//! rather than ASSERT to specify the expected results of tests.
#define ASSERT(exp) \
    do { \
        if (!(exp)) \
            FAIL("FAILED assertion '" << #exp << "'"); \
    } while (0)
#define ASSERT(exp) \
  do { \
    if (!(exp)) \
      FAIL("FAILED assertion '" << #exp << "'"); \
  } while (0)

#define CONFIRM(exp) \
  do { \
    if (!(exp)) \
      FAIL("FAILED to confirm '" << #exp << "'"); \
    else \
      OUTL("OK" << CODE_LOC); \
  } while (0)


#define CONFIRM_ASSERT(exp,match) \
  do { \
    bool stack = ThrowOnFailure; \
    try { \
      ThrowOnFailure = true; \
      exp; \
      ThrowOnFailure = stack; \
      FAIL("no assertion"); \
    } \
    catch(std::string &msg) { \
      ThrowOnFailure = stack; \
      CONFIRM(strstr(msg.c_str(),match)); \
    } \
  } while(0)

#define RETURN_ASSERT(exp) \
    do { \
        if ( !(exp ) ) \
        { \
            DEBUG(ALWAYS,"FAILED assertion '"  #exp << "'" << CODE_LOC); \
            return false; \
        } \
    } while(0)
    
#define RETURN_FALSE_ON_BAD_FILE(path) \
    do \
    { \
        std::ifstream infile(path); \
        if ( !infile.good() ) { \
            DEBUG(ALWAYS,"can not open " \
                << DUMP(path) \
                << DUMP(errno) \
                << " " \
                << strerror(errno)); \
            return false; \
        } \
    } while (0)
    




//------------------------------------------------------------------
// DEBUG facility
//------------------------------------------------------------------
#define DEBUG(flag,exp) \
    do { \
        if (DEBUG_##flag)  { \
            std::ostringstream os; \
            os << "DEBUG(" << #flag << "): " << exp; \
            pthread_mutex_lock(&artDisplay::debugMutex) ; \
            OUTL(os.str()); \
            pthread_mutex_unlock(&artDisplay::debugMutex) ; \
        } \
    } while (0)
#define DEBUG_ALWAYS true
#define DEBUG_NEVER false

// an alias for ALWAYS to simplify grepping potentially significant 
// events from log files, but to avoid the string ERROR, which may
// be used to trigger immediate human intervention
#define DEBUG_REVIEW true

#endif /* BASICS_H_ */
