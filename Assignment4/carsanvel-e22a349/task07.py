# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15pGolb5bl9ED8DxggBXkfIYjjzzBlrdD

**Task 07: Querying RDF(s)**
"""

# !pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

ns = Namespace("http://somewhere#")

# With RDFLib

def subClasses(Class):
  for s, p, o in g.triples((None, RDFS.subClassOf, Class)):
    subClasses(s)
    print(s)

subClasses(ns.Person)

# With SPARQL

q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?Subject rdfs:subClassOf+ ns:Person 
  }
  ''', initNs = {
      "ns":ns,
      "rdfs":RDFS
  }
)

for r in g.query(q1):
  print(r.Subject)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# With RDFLib

def personIndividuals(Class):
  for s, p, o in g.triples((None, RDF.type, Class)):
    print(s)
  for s, p, o in g.triples((None, RDFS.subClassOf, Class)):
    personIndividuals(s)


personIndividuals(ns.Person)

# With SPARQL
# Al utilizar el operador * con rdfs:subClassOf, ya se incluye la propia clase
# Person, por eso no se han hecho dos consultas y un UNION
q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?class rdfs:subClassOf* ns:Person .
    ?Subject a ?class
  }
  ''', initNs = {
      "ns":ns,
      "rdfs":RDFS
  }
)

for r in g.query(q1):
  print(r.Subject)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

# With RDFLib

def personIndividualsProperties(Class):
  for s, p, o in g.triples((None, RDF.type, Class)):
    for s2, p2, o2 in g.triples((s, None, None)):
      print(s2, p2, o2)
  for s, p, o in g.triples((None, RDFS.subClassOf, Class)):
    personIndividualsProperties(s)


personIndividualsProperties(ns.Person)

# With SPARQL

q1 = prepareQuery('''
  SELECT ?Subject ?prop ?value WHERE { 
    ?class rdfs:subClassOf* ns:Person .
    ?Subject a ?class .
    ?Subject ?prop ?value
  }
  ''', initNs = {
      "ns":ns,
      "rdfs":RDFS
  }
)

for r in g.query(q1):
  print(r.Subject, r.prop, r.value)