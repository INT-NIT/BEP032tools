AnDO package
============
The Animal Data Organization (AnDO) is a set of specifications for the organization of a directory containing experimental data recorded in animals. It is very inspired by the BIDS specifications ( https://bids-specification.readthedocs.io ). The main difference lies in the fact that in experiments conducted with animals, it is very common to have different settings for different sessions, and more importantly for different animals (whereas research on human subjects tends to have exactly the same protocol used for all subjects, as looked after by the BIDS specifications).

It follows a hierarchy of directories matched with the following concepts, as they are used in research studies conducted with animal models:

- Dataset, A set of experimental data acquired for the purpose of a particular study / experiment. It is composed of data acquired in one or more animals, with one or more sessions recorded in each animal.
- Subject, An animal that was included in the study.
- Session, A temporal grouping of experimental data recorded in a given animal, on a given day. There can be several sessions on the same day if the recording settings are modified between sessions or if the recording needs to be interrupted and restarted.

We describe below the set of specifications themselves, as well as an application -- the AnDOChecker -- that was developed to check whether a directory given as input respects the AnDO.

Packages
-----------

.. toctree::
   :maxdepth: 10


   ando.tools


ando.AnDOChecker module
-----------------------

.. automodule:: ando.AnDOChecker
   :members:
   :undoc-members:
   :show-inheritance:


