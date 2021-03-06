rpm_deps
========

Utility to output Graphviz dot graphs of rpm dependencies


usage
=====

To see the dependencies of an installed package
  $> ./rpm_deps_graph.py <pkg_name>

To see the dependencies of an RPM
  $> ./rpm_deps_graph.py ./XXXX-0.0.1-1.rpm

To see the build dependencies of a SRPM
  $> ./rpm_deps_graph.py ./XXXX-0.0.1-1.src.rpm

If you are calling against an RPM file, this tool expects to 
resolve the dependencies from the system's RPM database.


License
=======

copyright (c) 2012 Vincent Batts <vbatts@hashbangbash.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

