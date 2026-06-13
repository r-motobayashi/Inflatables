
#ifndef MESHFEM_EXPORT_H
#define MESHFEM_EXPORT_H

#ifdef MESHFEM_STATIC_DEFINE
#  define MESHFEM_EXPORT
#  define MESHFEM_NO_EXPORT
#else
#  ifndef MESHFEM_EXPORT
#    ifdef MeshFEM_EXPORTS
        /* We are building this library */
#      define MESHFEM_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define MESHFEM_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef MESHFEM_NO_EXPORT
#    define MESHFEM_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef MESHFEM_DEPRECATED
#  define MESHFEM_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef MESHFEM_DEPRECATED_EXPORT
#  define MESHFEM_DEPRECATED_EXPORT MESHFEM_EXPORT MESHFEM_DEPRECATED
#endif

#ifndef MESHFEM_DEPRECATED_NO_EXPORT
#  define MESHFEM_DEPRECATED_NO_EXPORT MESHFEM_NO_EXPORT MESHFEM_DEPRECATED
#endif

/* NOLINTNEXTLINE(readability-avoid-unconditional-preprocessor-if) */
#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef MESHFEM_NO_DEPRECATED
#    define MESHFEM_NO_DEPRECATED
#  endif
#endif

#endif /* MESHFEM_EXPORT_H */
