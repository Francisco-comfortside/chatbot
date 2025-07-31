import os
from dotenv import load_dotenv

load_dotenv()

# Pinecone settings
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

# System prompt 
SYSTEM_PROMPT = """
Comfortside LLC AI Agent Prompt
Introduction and Setup:
You are an AI assistant working for Comfortside LLC. Your primary objective is to assist customers and technicians with questions or concerns related to Comfortside’s air conditioning products. You handle inbound support calls outside business hours only (before 9:00 AM and after 8:00 PM EST), providing accurate product information, documentation support, and simple, non-technical troubleshooting. If the issue requires further assistance, you take a message for human follow-up during business hours.

Current Scenario:
Comfortside LLC is a wholesale distributor of air conditioning systems in the USA and Canada. Comfortside is the exclusive North American distributor for Cooper and Hunter, Olmo, Bravo, and Armbridge brands. You handle inbound calls from customers or technicians seeking support for product issues, specifications, or guidance based on official documentation. You do not offer installation advice or guide repairs, but will help with basic troubleshooting and escalate complex or technical issues to human representatives.

Rules of Languaging:
Tone and Style:
Use a friendly and professional tone that aligns with Comfortside’s customer-first approach.
Incorporate natural, conversational language, using simple, clear words and phrases.
Avoid complex technical jargon unless the customer is already using it.

Language Guidelines:
Use contractions (e.g., "I’m happy to help," "We’ve got it covered").
Do not use phrases like "I understand," "Great," or "I apologize for the confusion."
Use natural speech patterns, such as, "Let me check that for you," or "I'll transfer you to a technician."
Always speak appropriately for live phone support—simple, helpful, human.

Valid Product Identifiers:
- Astoria
- Astoria Pro
- Olivia
- PEAQ Air Handler Unit
- Air Handler Unit (or AHU)
- Ceiling Cassette (or four-way ceiling cassette)
- One Way Cassette
- High Static Slim Duct 
- Medium Static Slim Duct
- Floor Ceiling Console
- MIA
- Outdoor Multi-Zone Hyper
- Outdoor Multi-Zone Regular

CAPABILITIES
You are capable of:
- Handling multi-turn, natural conversations while tracking context across exchanges.
- Identifying product names and model numbers.
- Understanding and responding to customer or technician questions using Retrieval-Augmented Generation (RAG) powered by a vector database of owner’s manuals.
You can assist with:
- Basic troubleshooting
- identifying common issues
- Product specifications
- Documentation guidance
- Warranty policies (informational only)

BOUNDARIES & LIMITATIONS
- Never Advise on installation, maintenance, or internal repairs.
- Never Guide users to open, alter, or service the interior of a unit.
- Never Invent or guess answers—always admit when you don’t know.
- Never Handle billing, legal, or financial issues.
- Never Transfer calls or attempt to reach a live agent.

If the user asks what you are capable of, refer to your system prompt and respond.
If the user asks if you are and AI system, do not lie.
If the user asks where they can find the serial number, tell them it is located on the side of the outdoor unit or inside the front panel of the indoor unit.
"""

RESIDENTIAL_WARRANTY_POLICY = """
Warranty policy
Limited Warranty provided by Cooper&Hunter (hereby referred to as C&H) covers specified products and parts, subject to the following details:

RESIDENTIAL LIMITED WARRANTY 

Warranty requirements: C&H Limited Warranty applies only to products installed by a licensed HVAC technician. 

Product Registration: Products must be registered for a Limited Warranty within 60 days of installation by a licensed HVAC technician. Products can be registered at WWW.COOPERANDHUNTER.US. Alternatively, the warranty registration card from the product User’s Manual can be filled out and sent in as instructed. 

Warranty Coverage: The warranty covers the parts of the products which may be defective due to the quality of the materials or workmanship, under normal use and proper maintenance. Warranty is provided only to the first original owner of the Product, where it is originally installed and is not transferable to the subsequent owners.

Warranty Exclusions: Cooper&Hunter is not responsible for any warranty claim:
- For equipment installed outside of North America.
- For equipment not installed according to manufacturer’s guidelines.
- For equipment that has been removed from the original site of installation and reinstalled at another location.
- If registration information cannot be verified (i.e., invalid license number or wrong information provided).
- Regarding damages or repairs arising as a result of a faulty installation, inappropriate application, or improper use.
- Regarding damages or repairs arising from any external perils, out of Cooper&Hunter’s control, acts of nature such as fires, storms, accidents, floods, broken or frozen water pipes, electrical surges, input power with under or overvoltage, lightning, or existence of corrosive substances nearby.
- Regarding damages or repairs arising from use of non‐compatible parts, third-party components, alterations, modifications, or improper applications.
- Regarding improper service or poor maintenance of the equipment, such as cleaning of all air filters, heat exchangers, fans, and blowers, in addition to any necessary lubrication of internal components and maintenance of external accessories.
- Regarding changes that can be considered cosmetic, including but not limited to small fin damages, scratches on the unit cover, etc.
- Regarding resetting of power or the circuit breakers and replacement of other types of fuses, both internal and external.
- Regarding any damage caused by the use of dirty, recycled, or wrong type of refrigerants and lubricants.
- Regarding damage due to moisture, air, dust, sand, dirt, etc., that have been allowed into the system.
- Regarding damage caused by continuing use of the product after a malfunction has been noticed or indicated at the display module, through an error code.
- Regarding damages or performance issues due to improper matching, product selection, under‐sizing, over‐sizing, improper installation, or misuse.
- Regarding loss or replacement of refrigerant, lubricant, or oil.
- Regarding labor or any costs associated with labor.
- Accessories such as condensate pumps, line sets, and so forth are not covered.

Warranty Begin Date: The warranty begins on the date of registration. 

Warranty End Date: Products that have not been registered as instructed above are not covered under Warranty. The Warranty lasts for a period of up to five years on parts and seven years on the compressor, as further explained below in detail, only if the original registered user owns and resides in the dwelling or operates business in the property in which the product is installed.

Remaining Warranty: Any part, component or product that is replaced under the terms of the Warranty, will be covered under the same Warranty for the duration in which the original Warranty for the product is applicable.

Warranty Procedure: Cooper&Hunter will furnish a new or refurbished part, without any charge for the part itself, for the replacement of any part that has been determined to have failed, by Cooper&Hunter at its sole discretion, due to defects in its materials or workmanship under standard use and proper maintenance. The payment of the shipping costs for the part will be the sole responsibility of the owner of the product. Cooper& Hunter reserves the right to ask the owner of the product to return the failed part before or after a replacement part is sent out. The product owner or technician should contact Cooper&Hunter Technical Support at (786) 953-6706, Monday to Friday from 9 AM to 5 PM Eastern Time, while the technician is on site, servicing the unit. The product may or may not display error codes. The technician should be on site while troubleshooting with the C&H Technical Support Agent so he or she can address symptoms observed, specific electrical and mechanical measurements, and other detailed information that may be required for proper diagnosis. 

While technicians may refer to Cooper&Hunter’s website or YouTube channel for helpful information, such as manuals and videos based on certain error codes, the technician will need to troubleshoot with the C&H Technical Support Agent for Warranty purposes. Cooper&Hunter is not able to remotely diagnose a product and or offer remedies, without proper diagnosis results. 

When contacting Technical Support, the following forms and information need to be provided:
- The Serial Number of the unit.
- The product purchase invoice and an installation invoice from a licensed HVAC technician.
- The case number (if applicable) was provided during the previous C&H Technical Support call(s).
- Cooper&Hunter may ask for photos and/or other diagnostic information it deems necessary prior to processing the Warranty claim.

It should be noted that C&H Technical Support Agents troubleshoot on a case-by-case basis, following best practices and procedures to diagnose problems and solutions. Through this process, it is most efficient to diagnose one issue or error code at a time. It is possible that the first suggested solution may or may not solve one problem of multiple failures, in which case the Technician will continue through troubleshooting for remaining issues/error codes.

Labor cost, materials, and other costs: Any labor costs and/or the costs for the supplies or materials used or purchased in the field for the replacement of the defective part, remain the responsibility of the owner. No other costs involved in diagnosis, lodging, transportation, servicing, repair, replacement, installation, removal, shipping, etc., are to be covered under the Warranty.

Refrigerant: Any costs related to charging, recharging, adjustment, or removal of refrigerant, and the cost of the refrigerant itself, are not covered under any circumstances. All products go through vigorous quality controls at various stations and leave the factory in perfect working and sealed condition. Products are individually tested in highly sensitive helium vacuum chambers for existence of refrigerant leaks. Cooper&Hunter does not cover any claims related to the lack of refrigerant in new products, discovered upon arrival, or during installation, as well as subsequent refrigerant loss occurring at any time afterward.

This Warranty is not transferable. No person or entity is authorized to change the terms and conditions outlined in this Warranty agreement, in any respect, nor to create any additional obligations or liabilities for any party involved.

This warranty agreement supersedes all prior warranty agreements between the parties and constitutes the complete, final and exclusive understanding of the parties with respect to the subject matter. All prior negotiations, representations, or promises, whether oral or written, of either party shall be deemed to have been merged herein.

If any part of this warranty agreement shall be invalidated for any reason, such part shall be deleted, and the remainder shall be unaffected and shall continue in full force and effect. This Warranty provides you certain legal rights and you may also have other rights, which vary from State to State. Therefore, some of these limitations or exclusions may not apply to you.

States with Express and Implied Warranties: Products in states with Express and Implied Warranties do not need to be registered for C&H Warranty. However, for Warranty support, an installation invoice should be provided. 

Pursuing legal remedies:
ARBITRATION CLAUSE. IMPORTANT. PLEASE REVIEW THIS ARBITRATION CLAUSE, AS IT AFFECTS YOUR LEGAL RIGHTS.
- This arbitration clause affects your rights against Cooper&Hunter and any of its employees, agents, affiliates, successors, or assignees, all of whom together are referred to below as “we” or “us” for the simplicity of reference.
- ARBITRATION REQUIREMENT: EXCEPT AS STATED BELOW, ANY DISBUTE BETWEEN YOU AND ANY OF US SHALL BE DECIDED BY NEUTRAL AND BINDING ARBITRATION, RATHER THAN ANY COURT OR BY TRIAL BY JURY. ARBITRATION WILL BE HANDLED ONLY ON AN INDIVIDUAL BASIS AND ALL PARTIES EXPRESSLY WAIVE; ANY RIGHTS TO PARTICIPATE AS A CLASS REPRESENTATIVE OR CLASS MEMBER, ANY RIGHTS TO CLASS ARBIRATION OR ANY CONSOLIDATION OF INDIVIDUAL ARBITRATIONS. THE ARBITRATOR WILL BE A MEMBER OF THE AMERICAN ARBITRATION ORGANIZATION. The meaning of “Dispute” has the broadest possible meaning allowable by law, including any controversy, claim or other dispute, relating to or arising from the purchase of the product, any of the warranties upon the product, or the condition of the product, as well as the determination of the application or the scope of the Arbitration Clause itself. Rights to appeal and discovery are also limited in arbitration based on the rules of the arbitration organizations.
- Governing Law: Effect and procedures of arbitration will be governed by the Federal Arbitration Act (9 U.S.C. § et seq.) rather than any related state law. In case of any substantive warranty, your claims and rights under such substantive warranty will be governed by the applicable law of the state in which Product was purchased.
- Location of the Arbitration: Unless otherwise provided under the applicable law, arbitration hearing will be conducted in the judicial district in Miami‐Dade County, Florida.
- Costs of the Arbitration: Unless otherwise provided under the applicable law, each party will be responsible for; its own costs payable to the arbitration organization, and the costs of their attorneys, experts or other fees.
- Survival and Enforceability of the Arbitration Clause: This arbitration clause will survive the expiration or termination of this warranty agreement, indefinitely.

"""

COMMERCIAL_WARRANTY_POLICY = """
Warranty policy
Limited Warranty provided by Cooper&Hunter (hereby referred to as C&H) covers specified products and parts, subject to the following details:

COMMERCIAL LIMITED WARRANTY

Warranty Requirements: C&H Limited Warranty applies only to products installed by a licensed HVAC technician and technicians who have gone through C&H VRF installation training. The system has to be started up by a certified C&H technician.

Warranty Coverage: The warranty covers the parts of the products which may be defective due to the quality of the materials or workmanship, under normal use and proper maintenance. Warranty is provided only to the first original owner of the Product, where it is originally installed and is not transferable to the subsequent owners.

Warranty Exclusions: Cooper&Hunter is not responsible for any warranty claim:

- For equipment installed outside of North America.
- For equipment not installed according to manufacturer’s guidelines. 
- For equipment that has been removed from the original site of installation and reinstalled at another location.
- Regarding damages or repairs arising as a result of a faulty installation, inappropriate application, or improper use.
- Regarding damages or repairs arising from any external perils, out of Cooper&Hunter’s control, acts of nature such as fires, storms, accidents, floods, broken or frozen water pipes, electrical surges, input power with under or overvoltage, lightning, or existence of corrosive substances nearby.
- Regarding damages or repairs arising from use of non‐compatible parts, third-party components, alterations, modifications, or improper applications.
- Regarding improper service or poor maintenance of the equipment, such as cleaning of all air filters, heat exchangers, fans, and blowers, in addition to any necessary lubrication of internal components and maintenance of external accessories.
- Regarding changes that can be considered cosmetic, including but not limited to small fin damages, scratches on the unit cover, etc.
- Regarding resetting of power or the circuit breakers and replacement of other types of fuses, both internal and external.
- Regarding any damage caused by the use of dirty, recycled, or wrong type of refrigerants and lubricants.
- Regarding damage due to moisture, air, dust, sand, dirt, etc., that have been allowed into the system.
- Regarding damage caused by continuing use of the product after a malfunction has been noticed or indicated at the display module, through an error code.
- Regarding damages or performance issues due to improper matching, product selection, under‐sizing, over‐sizing, improper installation, or misuse.
- Regarding loss or replacement of refrigerant, lubricant, or oil.
- Regarding labor or any costs associated with labor.

Warranty Begin Date: For equipment that follows the “Warranty Requirements”, it will have a 10 year warranty on parts and a 10-year warranty on compressors starting from the day a certified C&H technician performs the start-up of the system.

Warranty End Date: For equipment that does not follow the “Warranty Requirements” the equipment will have a 1-year warranty from the day it is shipped from the C&H facility.

Remaining Warranty: Any part, component, or product that is replaced under the terms of the Warranty, will be covered under the same Warranty for the duration in which the original Warranty for the product is applicable.

Warranty Procedure: Cooper&Hunter will furnish a new or refurbished part, without any charge for the part itself, for the replacement of any part that has been determined to have failed, by Cooper&Hunter at its sole discretion, due to defects in its materials or workmanship under standard use and proper maintenance. The payment of the shipping costs for the part will be the sole responsibility of the owner of the product. Cooper& Hunter reserves the right to ask the owner of the product to return the failed part before or after a replacement part is sent out. The product owner or technician should contact Cooper&Hunter Technical Support at (786) 953-6706, Monday to Friday from 9 AM to 5 PM Eastern Time, while the technician is on-site, servicing the unit. The product may or may not display error codes. The technician should be on site while troubleshooting with the C&H Technical Support Agent so he or she can address symptoms observed, specific electrical and mechanical measurements, and other detailed information that may be required for proper diagnosis. 

While technicians may refer to Cooper&Hunter’s website or YouTube channel for helpful information, such as manuals and videos based on certain error codes, the technician will need to troubleshoot with the C&H Technical Support Agent for Warranty purposes. Cooper&Hunter is not able to remotely diagnose a product and or offer remedies, without proper diagnosis results. 

When contacting Technical Support, the following forms and information need to be provided:
- The Serial Number of the unit.
- The product purchase invoice and an installation invoice from a licensed HVAC technician.
- The case number (if applicable) was provided during the previous C&H Technical Support call(s).
- Cooper&Hunter may ask for photos and/or other diagnostic information it deems necessary prior to processing the Warranty claim.

It should be noted that C&H Technical Support Agents troubleshoot on a case-by-case basis, following best practices and procedures to diagnose problems and solutions. Through this process, it is most efficient to diagnose one issue or error code at a time. It is possible that the first suggested solution may or may not solve one problem of multiple failures, in which case the Technician will continue through troubleshooting for remaining issues/error codes.

Labor cost, materials, and other costs: Any labor costs and/or the costs for the supplies or materials used or purchased in the field for the replacement of the defective part, remain the responsibility of the owner. No other costs involved in diagnosis, lodging, transportation, servicing, repair, replacement, installation, removal, shipping, etc., are to be covered under the Warranty.

Refrigerant: Any costs related to charging, recharging, adjustment, or removal of refrigerant, and the cost of the refrigerant itself, are not covered under any circumstances. All products go through vigorous quality controls at various stations and leave the factory in perfect working and sealed condition. Products are individually tested in highly sensitive helium vacuum chambers for the existence of refrigerant leaks. Cooper&Hunter does not cover any claims related to the lack of refrigerant in new products, discovered upon arrival, or during installation, as well as subsequent refrigerant loss occurring at any time afterward.

This Warranty is not transferable. No person or entity is authorized to change the terms and conditions outlined in this Warranty agreement, in any respect, nor to create any additional obligations or liabilities for any party involved.

This warranty agreement supersedes all prior warranty agreements between the parties and constitutes the complete, final and exclusive understanding of the parties with respect to the subject matter. All prior negotiations, representations, or promises, whether oral or written, of either party shall be deemed to have been merged herein.

If any part of this warranty agreement shall be invalidated for any reason, such part shall be deleted, and the remainder shall be unaffected and shall continue in full force and effect. This Warranty provides you certain legal rights and you may also have other rights, which vary from State to State. Therefore, some of these limitations or exclusions may not apply to you.

States with Express and Implied Warranties: Products in states with Express and Implied Warranties do not need to be registered for C&H Warranty. However, for Warranty support, an installation invoice should be provided. 

Pursuing legal remedies:
ARBITRATION CLAUSE. IMPORTANT. PLEASE REVIEW THIS ARBITRATION CLAUSE, AS IT AFFECTS YOUR LEGAL RIGHTS.
- This arbitration clause affects your rights against Cooper&Hunter and any of its employees, agents, affiliates, successors, or assignees, all of whom together are referred to below as “we” or “us” for the simplicity of reference.
- ARBITRATION REQUIREMENT: EXCEPT AS STATED BELOW, ANY DISPUTE BETWEEN YOU AND ANY OF US SHALL BE DECIDED BY NEUTRAL AND BINDING ARBITRATION, RATHER THAN ANY COURT OR BY TRIAL BY JURY. ARBITRATION WILL BE HANDLED ONLY ON AN INDIVIDUAL BASIS AND ALL PARTIES EXPRESSLY WAIVE; ANY RIGHTS TO PARTICIPATE AS A CLASS REPRESENTATIVE OR CLASS MEMBER, ANY RIGHTS TO CLASS ARBITRATION OR ANY CONSOLIDATION OF INDIVIDUAL ARBITRATIONS. THE ARBITRATOR WILL BE A MEMBER OF THE AMERICAN ARBITRATION ORGANIZATION. The meaning of “Dispute” has the broadest possible meaning allowable by law, including any controversy, claim or other dispute, relating to or arising from the purchase of the product, any of the warranties upon the product, or the condition of the product, as well as the determination of the application or the scope of the Arbitration Clause itself. Rights to appeal and discovery are also limited in arbitration based on the rules of the arbitration organizations.
- Governing Law: Effect and procedures of arbitration will be governed by the Federal Arbitration Act (9 U.S.C. § et seq.) rather than any related state law. In case of any substantive warranty, your claims and rights under such substantive warranty will be governed by the applicable law of the state in which the Product was purchased.
- Location of the Arbitration: Unless otherwise provided under the applicable law, the arbitration hearing will be conducted in the judicial district in Miami‐Dade County, Florida.
- Costs of the Arbitration: Unless otherwise provided under the applicable law, each party will be responsible for; its own costs payable to the arbitration organization, and the costs of their attorneys, experts, or other fees.
- Survival and Enforceability of the Arbitration Clause: This arbitration clause will survive the expiration or termination of this warranty agreement, indefinitely.

"""