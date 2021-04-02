.. andO documentation master file, created by
   sphinx-quickstart on Tue Mar 30 14:48:19 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the AnDO project
===========================

March 2021

The Animal Data Organization (AnDO) is a project initiated at the Institut de Neurosciences de la Timone, in Marseille, France, in order to set up a standardization of the experimental data recorded in animal models. Since its launch in early 2020, its aims have significantly evolve following these axes:

 - first, we have opened our desire for standardization to the community through the launch of a Working Group endorsed by the INCF; please feel free to join the group to participate in this effort: https://www.incf.org/sig/incf-working-group-standardized-data ; we are meeting approximately every two months and we are making progress in subgroups on well defined issues between each meeting;

 - secondly, after discussions within the group, we have initiated a specific standardization effort for electrophysiology, as a BIDS Extension Proposal (BEP32: https://bids.neuroimaging.io/get_involved.html ); we are actively looking for feedback from the community on this proposal, so feel free to directly comment in the document that details the data and metadata organization: http://bit.ly/BIDS-animal-ephys.

At this moment, this repository provides several tools, amongst which a validator (the AnDOChecker) which complies to the latest specifications described in the BEP32 document. We are committed to 




Example of an AnDO Repository
--------------------------

.. image:: _static/examples.png
  :width: 400
  :align: center
  :alt: Alternative text


Tools
===========================
AnDOChecker :
   - Further information here  :ref:`to_checker`.

   - Checks the validity of a data set with respect to the BIDS-animal-ephys BEP specifications. The specifications that define what is checked by this function is available in the following document: https://docs.google.com/document/d/1oG-C8T-dWPqfVzL2W8HO3elWK8NIh2cOCPssRGv23n0

AnDOGenerator :
   - Further information here  :ref:`to_generator`.

   - Generate a BIDS-animal-ephys folder structure that follows the BEP specifcations with a overveiw CSV files and optional metadata files as input.

-----------

.. toctree::
   :maxdepth: 10
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
