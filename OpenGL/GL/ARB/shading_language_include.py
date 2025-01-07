'''OpenGL extension ARB.shading_language_include

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.shading_language_include to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension introduces a #include GLSL directive to allow reusing
	the same shader text in multiple shaders and defines the semantics
	and syntax of the names allowed in #include directives. It also
	defines API mechanisms to define the named string backing a
	#include.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/shading_language_include.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.shading_language_include import *
from OpenGL.raw.GL.ARB.shading_language_include import _EXTENSION_NAME

def glInitShadingLanguageIncludeARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glNamedStringARB.name size not checked against namelen
# INPUT glNamedStringARB.string size not checked against stringlen
glNamedStringARB=wrapper.wrapper(glNamedStringARB).setInputArraySize(
    'name', None
).setInputArraySize(
    'string', None
)
# INPUT glDeleteNamedStringARB.name size not checked against namelen
glDeleteNamedStringARB=wrapper.wrapper(glDeleteNamedStringARB).setInputArraySize(
    'name', None
)
# INPUT glCompileShaderIncludeARB.length size not checked against count
# INPUT glCompileShaderIncludeARB.path size not checked against count
glCompileShaderIncludeARB=wrapper.wrapper(glCompileShaderIncludeARB).setInputArraySize(
    'length', None
).setInputArraySize(
    'path', None
)
# INPUT glIsNamedStringARB.name size not checked against namelen
glIsNamedStringARB=wrapper.wrapper(glIsNamedStringARB).setInputArraySize(
    'name', None
)
# INPUT glGetNamedStringARB.name size not checked against namelen
glGetNamedStringARB=wrapper.wrapper(glGetNamedStringARB).setInputArraySize(
    'name', None
).setOutput(
    'string',size=lambda x:(x,),pnameArg='bufSize',orPassIn=True
).setOutput(
    'stringlen',size=(1,),orPassIn=True
)
# INPUT glGetNamedStringivARB.name size not checked against namelen
glGetNamedStringivARB=wrapper.wrapper(glGetNamedStringivARB).setInputArraySize(
    'name', None
).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
### END AUTOGENERATED SECTION