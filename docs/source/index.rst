.. UiTdatabank documentation master file, created by
   sphinx-quickstart on Tue Aug  2 10:00:41 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======================================
Python wrapper voor UiTdatabank API v2
======================================

.. toctree::
   :maxdepth: 4

De UiTdatabank biedt een API om de databank te consulteren.
De API is uitgebreid beschreven in deze `handleiding <http://goo.gl/gRCJ5w>`_.

Om de API in Python te gebruiken kan je gebruik maken van de requests bibliotheek.
Om het authenticatie en zoekproces te vergemakkelijken schreef ik een lichte wrapper rond de API.

Voorbeeld
=========

>>> from uitdatabank.uitdatabank import UiTdatabank
>>> udb = UiTdatabank("settings.cfg")
>>> q, fq = udb.construct_event_query([("city", "Gent"), "AND", ("jazz")])
>>> params = udb.construct_parameters_for_api_call({"q": q, "fq": fq})
>>> searchresults = udb.find(params)
>>> print(searchresults.get_soonest_event())

Configuratie
============

De settings voor authenticatie en de API basisurl worden aangegeven in een settings file die de volgende structuur heeft:
 ::

     [oauth]
     app_key = BAAC107B-632C-46C6-A254-13BC2CE19C6C
     app_secret = ec9a0e8c2cdc52886bc545e14f888612
     user_token =
     user_secret =

     [uitdatabank]
     url = https://www.uitid.be/uitid/rest/searchv2/search

Het pad naar die file wordt bij de initialisatie van de wrapper meegegeven als argument.

Overzicht van functionaliteit
=============================

Een overzicht van de klassen en functies vind je hier:

:ref:`modindex`


Contact
=======

Issues, feature request op `github <https://github.com/ruettet/uitdatabank>`_.