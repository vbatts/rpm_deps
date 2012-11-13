#!/usr/bin/env python
'''
take an argument of a package
determine its deps, and so on.
optionally generate a dot diagram of the dep tree.
'''

import os
import sys
import rpm


'''
name=h['name'],
version=h['version'],
release=h['release'],
arch=h['arch'],
epoch=h['epoch'] or 0,
vendor=h['vendor'] or None
'''

class Package():
    '''
    a node in the dependency tree
    '''
    def __init__(self,
            name,
            version = None,
            arch = None,
            requires = [],
            provides = []):

        self.name = name
        self.version = version
        self.arch = arch
        self.requires = requires
        self.provides = provides

        # this will be references to other Packages
        self.deps = set()

def what_requires(plist, prov):
    '''
    return a list of the packages that require the provided string +prov+
    '''
    return filter( lambda x: prov in x.requires, plist)

def what_provides(plist, req):
    '''
    return a list of the packages that are or provide +req+
    '''
    ret_list = filter( lambda x: req in x.provides, plist)
    ret_list += filter( lambda x: req == x.name, plist)
    return ret_list

def mkpkg(pkg_hdr):
    '''
    make a Package from an RPM package header
    '''
    return Package(
            pkg_hdr[rpm.RPMTAG_NAME],
            pkg_hdr[rpm.RPMTAG_VERSION],
            pkg_hdr[rpm.RPMTAG_ARCH],
            pkg_hdr[rpm.RPMTAG_REQUIRES],
            pkg_hdr[rpm.RPMTAG_PROVIDES],
            )

def get_pkg_list(ts = rpm.TransactionSet()):
    '''
    return a list of the packages in the system RPM database
    '''
    ts.setVSFlags(-1)
    installed = ts.dbMatch()
    pkg_list = []

    for p in installed:
        #print fmt_pkg(p)
        pkg_list.append(mkpkg(p))

    return pkg_list

def build_dep_tree(plist, root, seen = set()):
    '''
    populate the dep list in the root node, given the package list
    '''
    if root.name in seen: return
    else: seen.add(root.name)

    for req in root.requires:
        for pkg in what_provides(plist, req):
            if pkg not in root.deps: root.deps.add(pkg)

    for dep in root.deps:
        build_dep_tree(plist, dep)
    
def print_dep_tree(root, indent = 0, seen = set()):
    if root.name in seen: return
    else: seen.add(root.name)

    print "%s%s: " % (" " * indent, root.name),
    print map(lambda x: x.name, root.deps)
    for dep in root.deps:
        print_dep_tree(dep, indent + 1)

def print_dot_link(root, seen = set(), inc = 0, directed = True):
    if root.name in seen: return
    else: seen.add(root.name)

    sep = "->" if directed else "--"
    for pkg in root.deps:
        print "\t\"%s\" %s \"%s\";" % ( root.name, sep, pkg.name )
        print_dot_link(pkg, seen, directed=directed)
    

def print_dot_dep_tree(root, directed = True):
    graph = "digraph" if directed else "graph"
    print "%s deps {" % (graph)
    print_dot_link(root, directed=directed)
    print "}"

def fmt_pkg(pkg_hdr):
    '''
    return a string with info from a package header object
    '''
    return "%s-%s\t%s" % ( pkg_hdr['name'],
            pkg_hdr['version'],
            ", ".join(pkg_hdr['requires']))

def readRpmHeader(ts, filename):
    """ Read an rpm header. """
    fd = os.open(filename, os.O_RDONLY)
    h = None
    try:
        h = ts.hdrFromFdno(fd)
    except rpm.error, e:
        if str(e) == "public key not available":
            print str(e)
        if str(e) == "public key not trusted":
            print str(e)
        if str(e) == "error reading package header":
            print str(e)
        h = None
    finally:
        os.close(fd)
    return h


if __name__ == '__main__':
    directed = True
    root = None

    if '-h' in sys.argv:
        print "%s [-D] <rpm|pkg_name>" % (sys.argv[0])
        exit(0)

    if '-D' in sys.argv:
        directed = False
        sys.argv.remove('-D')

    ts = rpm.TransactionSet()
    pkg_list = get_pkg_list(ts)
    if os.path.isfile(sys.argv[1]):
        hdr = readRpmHeader(ts, sys.argv[1])
        root = mkpkg(hdr)
    else:
        root = filter(lambda x: x.name == sys.argv[1], pkg_list)
        if len(root) != 1:
            print "ERROR: %s did not only return one result" % sys.argv[1]
            print map(lambda x: x.name, root)
            sys.exit(1)
        else:
            root = root[0]
    
    build_dep_tree(pkg_list, root)
    #print_dep_tree(root)
    print_dot_dep_tree(root, directed=directed)
    


