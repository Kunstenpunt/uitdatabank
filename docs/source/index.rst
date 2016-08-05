.. UiTdatabank documentation master file, created by
   sphinx-quickstart on Tue Aug  2 10:00:41 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================================
Python3 wrapper UiTdatabank APIv2
=================================

.. toctree::
   :maxdepth: 4

De UiTdatabank biedt een API om de databank te consulteren.
De API is uitgebreid beschreven in deze `handleiding <http://goo.gl/gRCJ5w>`_.

Om de API in Python te gebruiken kan je gebruik maken van de requests bibliotheek.
Om het authenticatie en zoekproces te vergemakkelijken schreef ik een lichte wrapper rond de API.

De wrapper is getest met python 3.4, maar zou ook voor python 2.7+ moeten werken.

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

De key/secret combinatie die hier wordt gedocumenteerd zijn de publieke keys voor demo- en testdoeleinden (augustus 2016).

Het pad naar deze file wordt bij de initialisatie van de wrapper meegegeven als argument.
De wrapper doet de rest.

Overzicht van functionaliteit
=============================

Een overzicht van de klassen en functies vind je hier:

:ref:`modindex`

Overzicht van de shortcuts
==========================

In :mod:`Shortcuts <uitdatabank.shortcuts.Shortcuts>` worden shortcuts naar frequente API calls verzameld.
Op dit moment zijn er nog niet veel shortcuts geimplementeerd, in afwachting van een typologie van API calls.
Een eerste probeersel, dat waarschijnlijk in een volgende versie zal verdwijnen:

* Zoeken naar events

  * toekomstige events op basis van de organisator
    :func:`find_upcoming_events_by_organiser_label <uitdatabank.shortcuts.Shortcuts.find_upcoming_events_by_organiser_label>`
  * toekomstige events op basis van de stad
    :func:`find_upcoming_events_by_city_name <uitdatabank.shortcuts.Shortcuts.find_upcoming_events_by_city_name>`


Contact
=======

Issues, feature request op `github <https://github.com/ruettet/uitdatabank>`_.