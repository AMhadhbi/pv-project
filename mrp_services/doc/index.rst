======================
Manufacturing Services
======================

************************************************************************************
November 15th, 2020 - this is a BETA release.  Please send feedback to ray@odoo.com.
************************************************************************************  

This is a "proof of concept" to illustrate how service products can be used in manufacturing orders to represent direct labor costs contributing to the cost of finished goods.

*****
Note:
*****

- This app may require changes before it is suitable to use in a production environment.
- It has only been tested in databases created with a country setting of the United States and may need localization outside the US.
- Discuss your requirements with an Odoo Advisor or Odoo Partner to understand the best way to leverage this functionality.

*************************************
Target Platform, Edition and Version:
*************************************

- Online, Odoo.sh or On-Premise.
- Enterprise Edition.  
- Version 14.0.  

**************
Required Apps:
**************

- Odoo Studio - web_studio
- Manufacturing - mrp
- Invoicing - account

*****************
Recommended Apps:
*****************

- Accounting - account_accountant

***********
Installing:
***********

1. Download the ZIP, do not unzip it.

2. From the Apps Switcher screen, toggle open Odoo Studio:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/odoo_studio_button.png

3. From the Customizations Menu on the left, select Import.

4. Upload the ZIP file and click IMPORT.

******
Setup:
******

- Create a Service product with a cost.

- Setup real-time inventory valuation for the product category of your finished goods.

- Add the service product to either a Bill of Materials or a Manufacturing Order.

************************
User Experience Changes:
************************
	
- A Services tab is added to the manufacturing order form view: 

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/services_tab.png

- The form view of service lines shows the unit cost of each service product and the amount that will be added to the finished product cost - based on the quantity of units consumed:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/services_line.png

- The Cost Analysis report available from completed manufacturing orders is hidden as it is unaware of service products (see Known Limitations for more information).

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/cost_analysis.png

*******************
Functional Changes:
*******************

- Service products on Bills of Materials are automatically added to the relevant manufacturing order.

- The unit cost of finished goods is increased based on the unit price of the service, the quantity of units of the service product consumed, and the quantity of finished goods completed in a given manufacturing order.

************
Walkthrough:
************

The following example requires the demo data installed.

- Create a Service Product

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/service_product.png

The Cost of this product will be added to the finished good cost based on how many units are consumed.

- Setup real-time inventory valuation on the Office Furniture product category:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/product_category.png

- Add a unit of the service product to the bill of materials for Plastic Laminate:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/components.png

- Create a new manufacturing order for this product.

- Consume a unit of the service product:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/consume.png

- Complete the manufacturing order and review the valuation (developer mode required):

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/valuation.png

*************************
Additional Functionality:
*************************

Accounting app:

- Just like additional direct costs from work centers, a balance in the Work in Progress account (if defined on the Production location) builds up each time a service product is consumed.

- Periodically, an accounting user should reclass this balance by using the Automatic Entries action:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/automatic_entries.png

- In this case, the $35 of labor (a credit) that has built up in WIP is reclassed to a Manufacturing Labor liability account:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/wizard.png

- The following entry is created:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/entry.png

- The new credit balance would then be cleared as part of the payroll process.

*****************
Scenarios Tested:
*****************

- Service Products with Units of Measure (such as hours) and costs that change over time.

- Manual and automated (such as reordering rules, make to order) creation of Manufacturing Orders.

- Manufacturing orders with additional services products added after creation.

- Warehouses with multiple steps setup to complete manufacturing operations.

******************
Known Limitations:
******************

- The Cost Analysis report on a manufacturing order is not aware of service products, so this report is hidden.

However:

- The BoM Structure & Cost report does show the complete projected cost, including labor, of the finished good:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/bom_structure_and_cost.png

- The Valuation button on the manufacturing order (developer model required) does show the correct finished good cost:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/14.0/mrp_services/doc/valuation.png

- The Journal Entry creating the finished goods does show the correct finished good cost.









