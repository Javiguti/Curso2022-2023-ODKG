# -*- coding: utf-8 -*-
"""ODKG - assignment 4 - task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a8E7E-QmJUceEjQe447bWFwc5In_c9KQ
"""

# -*- coding: utf-8 -*-
"""Task07.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1tV5j-DRcpPtoJGoMj8v2DSqR_9wyXeiE
**Task 07: Querying RDF(s)**
"""

!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/resources/example6.rdf", format="xml")

'''**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**'''
ns = Namespace("http://somewhere#")

from rdflib.plugins.sparql import prepareQuery

print("List all subclasses of \"Person\" via RDFLib:")
for s,p,o in g.triples((None,RDFS.subClassOf,ns.Person)):
    print(s)

print("List all subclasses of \"Person\" via SPARQL:")
q = prepareQuery('''
  SELECT ?Subject
  WHERE { 
    ?Subject rdfs:subClassOf ns:Person
  }
  ''',
  initNs = { "ns": ns, "rdfs": RDFS}
  )
for r in g.query(q):
  print(r.Subject)

'''**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**'''

print("List all individuals of \"Person\" via RDFLib:")
for s,p,o in g.triples((None, RDF.type, ns.Person)):
    print(s)

for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for sub,pre,obj in g.triples((None, RDF.type, s)):
        print(sub)

print("List all individuals of \"Person\" via SPARQL:")
q = prepareQuery('''
  SELECT ?Subject
  WHERE { 
    {?Subject rdf:type ns:Person} 
    UNION
    {
     ?Subclass rdfs:subClassOf ns:Person .
     ?Subject  rdf:type ?Subclass 
    }
  }
  ''',
  initNs = { "ns": ns, "rdf": RDF}
  )
for r in g.query(q):
  print(r.Subject)

'''**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**'''

print("List all individuals of \"Person\" and all their properties including their class via RDFLib:")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    for sub, pre, obj in g.triples((s, None, None)):
        print(sub, pre, obj)

for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for sub, pre, obj in g.triples((None, RDF.type, s)):
      for person, rel, subclass in g.triples((sub, None, None)):
        print(person, rel, subclass)        


print("List all individuals of \"Person\" and all their properties including their classvia SPARQL")
q = prepareQuery('''
  SELECT ?Subject ?Pre ?Obj
  WHERE {
    {?Subject rdf:type ns:Person .
     ?Subject ?Pre ?Obj
    }
    UNION 
    {
     ?Subclass rdfs:subClassOf ns:Person .
     ?Subject  rdf:type ?Subclass .
     ?Subject ?Pre ?Obj
    }
  }
  ''',
  initNs = { "ns": ns, "rdf": RDF}
)

for r in g.query(q):
  print(r.Subject, r.Pre, r.Obj)