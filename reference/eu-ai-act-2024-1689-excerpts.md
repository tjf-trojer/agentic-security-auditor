<!--
  THE SECOND ANCHOR, AND IT IS CONDITIONAL. These are verbatim excerpts of the
  articles this auditor is allowed to cite, and no others. They are cited only
  when the scope gate in method/scope-gate.md finds that the Act binds. If it
  does not bind, this file is not used and no finding refers to it.
-->

# Regulation (EU) 2024/1689 (EU AI Act): the articles this auditor may cite

> **Source.** Regulation (EU) 2024/1689 of the European Parliament and of the
> Council of 13 June 2024 laying down harmonised rules on artificial intelligence.
> Official Journal of the European Union, L series, 12 July 2024.
> EUR-Lex CELEX [32024R1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689),
> official English version.
>
> **Licence.** Commission Decision [2011/833/EU](https://eur-lex.europa.eu/eli/dec/2011/833/oj)
> on the reuse of Commission documents. Reuse for commercial and non-commercial
> purposes is permitted with acknowledgement of the source. See `../NOTICES.md`.
>
> **Provenance.** Extracted from the official PDF with pdfminer.six on
> 2026-06-25. Paragraph numbers sit on their own lines in places; that is an
> artifact of two-column PDF extraction, not an edit. No wording is altered.
>
> **Why this is an excerpt and not the whole Regulation.** The full consolidated
> text runs to 10,667 lines. An auditor that ships all of it and cites six
> articles is padding, not sourcing. What follows is every article this auditor
> is permitted to cite, complete and unabridged. The full text is one file away
> in the source named above if you want to check the surrounding context.
>
> **Authoritative version.** These excerpts are for checking a finding against
> the provision it cites. For any legal purpose, use the Official Journal text at
> the EUR-Lex link above.

---

## What is here, and why each article is in scope for an agent review

| Article | Subject | Why an agent auditor cites it |
|---|---|---|
| [Art. 3](#article-3) | Definitions | 3(1) is the "AI system" test; 3(23) is the substantial-modification rule that agent drift can trigger |
| [Art. 12](#article-12) | Record-keeping | The logging duty behind an observability finding |
| [Art. 14](#article-14) | Human oversight | The duty that a human can understand, intervene in, and stop the system |
| [Art. 25](#article-25) | Responsibilities along the AI value chain | The role flip: a deployer that changes purpose or behaviour becomes a provider |
| [Art. 26](#article-26) | Obligations of deployers of high-risk AI systems | What the reader of this audit personally owes if they deploy |
| [Art. 50](#article-50) | Transparency obligations | Binds by behaviour at any risk tier: disclosure to people, marking of synthetic output |
| [Art. 72](#article-72) | Post-market monitoring by providers | The lifetime-monitoring duty an unobservable agent cannot meet |
| [Annex III](#annex-iii) | High-risk use cases | The list the scope gate checks before saying a use is high-risk. Shipped because the gate asks the auditor to name a point, and `identity.md` forbids citing what is not here |

---


## Article 3

<!-- verbatim, lines 3359-3711 of the official English text -->

Article 3

Definitions

For the purposes of this Regulation, the following definitions apply:

(1)

‘AI system’ means a machine-based system that is designed to operate with varying levels of autonomy and that may
exhibit adaptiveness after deployment, and that, for explicit or implicit objectives, infers, from the input it receives,
how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or
virtual environments;

(2)

‘risk’ means the combination of the probability of an occurrence of harm and the severity of that harm;

(3)

(4)

(5)

(6)

(7)

‘provider’ means a natural or legal person, public authority, agency or other body that develops an AI system or
a general-purpose AI model or that has an AI system or a general-purpose AI model developed and places it on the
market or puts the AI system into service under its own name or trademark, whether for payment or free of charge;

‘deployer’ means a natural or legal person, public authority, agency or other body using an AI system under its
authority except where the AI system is used in the course of a personal non-professional activity;

‘authorised representative’ means a natural or legal person located or established in the Union who has received and
accepted a written mandate from a provider of an AI system or a general-purpose AI model to, respectively, perform
and carry out on its behalf the obligations and procedures established by this Regulation;

‘importer’ means a natural or legal person located or established in the Union that places on the market an AI system
that bears the name or trademark of a natural or legal person established in a third country;

‘distributor’ means a natural or legal person in the supply chain, other than the provider or the importer, that makes
an AI system available on the Union market;

(8)

‘operator’ means a provider, product manufacturer, deployer, authorised representative, importer or distributor;

46/144

ELI: http://data.europa.eu/eli/reg/2024/1689/oj


OJ L, 12.7.2024

EN

(9)

‘placing on the market’ means the first making available of an AI system or a general-purpose AI model on the Union
market;

(10) ‘making available on the market’ means the supply of an AI system or a general-purpose AI model for distribution or

use on the Union market in the course of a commercial activity, whether in return for payment or free of charge;

(11) ‘putting into service’ means the supply of an AI system for first use directly to the deployer or for own use in the Union

for its intended purpose;

(12) ‘intended purpose’ means the use for which an AI system is intended by the provider, including the specific context
and conditions of use, as specified in the information supplied by the provider in the instructions for use, promotional
or sales materials and statements, as well as in the technical documentation;

(13) ‘reasonably foreseeable misuse’ means the use of an AI system in a way that is not in accordance with its intended
purpose, but which may result from reasonably foreseeable human behaviour or interaction with other systems,
including other AI systems;

(14) ‘safety component’ means a component of a product or of an AI system which fulfils a safety function for that product
or AI system, or the failure or malfunctioning of which endangers the health and safety of persons or property;

(15) ‘instructions for use’ means the information provided by the provider to inform the deployer of, in particular, an AI

system’s intended purpose and proper use;

(16) ‘recall of an AI system’ means any measure aiming to achieve the return to the provider or taking out of service or

disabling the use of an AI system made available to deployers;

(17) ‘withdrawal of an AI system’ means any measure aiming to prevent an AI system in the supply chain being made

available on the market;

(18) ‘performance of an AI system’ means the ability of an AI system to achieve its intended purpose;

(19) ‘notifying authority’ means the national authority responsible for setting up and carrying out the necessary procedures

for the assessment, designation and notification of conformity assessment bodies and for their monitoring;

(20) ‘conformity assessment’ means the process of demonstrating whether the requirements set out in Chapter III, Section 2

relating to a high-risk AI system have been fulfilled;

(21) ‘conformity assessment body’ means a body that performs third-party conformity assessment activities, including

testing, certification and inspection;

(22) ‘notified body’ means a conformity assessment body notified in accordance with this Regulation and other relevant

Union harmonisation legislation;

(23) ‘substantial modification’ means a change to an AI system after its placing on the market or putting into service which
is not foreseen or planned in the initial conformity assessment carried out by the provider and as a result of which the
compliance of the AI system with the requirements set out in Chapter III, Section 2 is affected or results in
a modification to the intended purpose for which the AI system has been assessed;

(24) ‘CE marking’ means a marking by which a provider indicates that an AI system is in conformity with the requirements
set out in Chapter III, Section 2 and other applicable Union harmonisation legislation providing for its affixing;

(25) ‘post-market monitoring system’ means all activities carried out by providers of AI systems to collect and review
experience gained from the use of AI systems they place on the market or put into service for the purpose of
identifying any need to immediately apply any necessary corrective or preventive actions;

(26) ‘market surveillance authority’ means the national authority carrying out the activities and taking the measures

pursuant to Regulation (EU) 2019/1020;

ELI: http://data.europa.eu/eli/reg/2024/1689/oj

47/144


EN

OJ L, 12.7.2024

(27) ‘harmonised standard’ means a harmonised standard as defined in Article 2(1), point (c), of Regulation (EU)

No 1025/2012;

(28) ‘common specification’ means a set of technical specifications as defined in Article 2, point (4) of Regulation (EU)

No 1025/2012, providing means to comply with certain requirements established under this Regulation;

(29) ‘training data’ means data used for training an AI system through fitting its learnable parameters;

(30) ‘validation data’ means data used for providing an evaluation of the trained AI system and for tuning its non-learnable

parameters and its learning process in order, inter alia, to prevent underfitting or overfitting;

(31) ‘validation data set’ means a separate data set or part of the training data set, either as a fixed or variable split;

(32) ‘testing data’ means data used for providing an independent evaluation of the AI system in order to confirm the

expected performance of that system before its placing on the market or putting into service;

(33) ‘input data’ means data provided to or directly acquired by an AI system on the basis of which the system produces an

output;

(34) ‘biometric data’ means personal data resulting from specific technical processing relating to the physical, physiological

or behavioural characteristics of a natural person, such as facial images or dactyloscopic data;

(35) ‘biometric identification’ means the automated recognition of physical, physiological, behavioural, or psychological
human features for the purpose of establishing the identity of a natural person by comparing biometric data of that
individual to biometric data of individuals stored in a database;

(36) ‘biometric verification’ means the automated, one-to-one verification, including authentication, of the identity of

natural persons by comparing their biometric data to previously provided biometric data;

(37) ‘special categories of personal data’ means the categories of personal data referred to in Article 9(1) of Regulation (EU)

2016/679, Article 10 of Directive (EU) 2016/680 and Article 10(1) of Regulation (EU) 2018/1725;

(38) ‘sensitive operational data’ means operational data related to activities of prevention, detection, investigation or
prosecution of criminal offences, the disclosure of which could jeopardise the integrity of criminal proceedings;

(39) ‘emotion recognition system’ means an AI system for the purpose of identifying or inferring emotions or intentions of

natural persons on the basis of their biometric data;

(40) ‘biometric categorisation system’ means an AI system for the purpose of assigning natural persons to specific
categories on the basis of their biometric data, unless it is ancillary to another commercial service and strictly
necessary for objective technical reasons;

(41) ‘remote biometric identification system’ means an AI system for the purpose of identifying natural persons, without
their active involvement, typically at a distance through the comparison of a person’s biometric data with the
biometric data contained in a reference database;

(42) ‘real-time remote biometric identification system’ means a remote biometric identification system, whereby the
capturing of biometric data, the comparison and the identification all occur without a significant delay, comprising
not only instant identification, but also limited short delays in order to avoid circumvention;

(43) ‘post-remote biometric identification system’ means a remote biometric identification system other than a real-time

remote biometric identification system;

(44) ‘publicly accessible space’ means any publicly or privately owned physical place accessible to an undetermined number
of natural persons, regardless of whether certain conditions for access may apply, and regardless of the potential
capacity restrictions;

48/144

ELI: http://data.europa.eu/eli/reg/2024/1689/oj


OJ L, 12.7.2024

(45) ‘law enforcement authority’ means:

EN

(a) any public authority competent for the prevention, investigation, detection or prosecution of criminal offences or
the execution of criminal penalties, including the safeguarding against and the prevention of threats to public
security; or

(b) any other body or entity entrusted by Member State law to exercise public authority and public powers for the
purposes of the prevention, investigation, detection or prosecution of criminal offences or the execution of
criminal penalties, including the safeguarding against and the prevention of threats to public security;

(46) ‘law enforcement’ means activities carried out by law enforcement authorities or on their behalf for the prevention,
investigation, detection or prosecution of criminal offences or the execution of criminal penalties, including
safeguarding against and preventing threats to public security;

(47) ‘AI Office’ means the Commission’s function of contributing to the implementation, monitoring and supervision of AI
systems and general-purpose AI models, and AI governance, provided for in Commission Decision of 24 January
2024; references in this Regulation to the AI Office shall be construed as references to the Commission;

(48) ‘national competent authority’ means a notifying authority or a market surveillance authority; as regards AI systems
put into service or used by Union institutions, agencies, offices and bodies, references to national competent
authorities or market surveillance authorities in this Regulation shall be construed as references to the European Data
Protection Supervisor;

(49) ‘serious incident’ means an incident or malfunctioning of an AI system that directly or indirectly leads to any of the

following:

(a) the death of a person, or serious harm to a person’s health;

(b) a serious and irreversible disruption of the management or operation of critical infrastructure;

(c) the infringement of obligations under Union law intended to protect fundamental rights;

(d) serious harm to property or the environment;

(50) ‘personal data’ means personal data as defined in Article 4, point (1), of Regulation (EU) 2016/679;

(51) ‘non-personal data’ means data other than personal data as defined in Article 4, point (1), of Regulation (EU)

2016/679;

(52) ‘profiling’ means profiling as defined in Article 4, point (4), of Regulation (EU) 2016/679;

(53) ‘real-world testing plan’ means a document that describes the objectives, methodology, geographical, population and

temporal scope, monitoring, organisation and conduct of testing in real-world conditions;

(54) ‘sandbox plan’ means a document agreed between the participating provider and the competent authority describing
the objectives, conditions, timeframe, methodology and requirements for the activities carried out within the sandbox;

(55) ‘AI regulatory sandbox’ means a controlled framework set up by a competent authority which offers providers or
prospective providers of AI systems the possibility to develop, train, validate and test, where appropriate in real-world
conditions, an innovative AI system, pursuant to a sandbox plan for a limited time under regulatory supervision;

(56) ‘AI literacy’ means skills, knowledge and understanding that allow providers, deployers and affected persons, taking
into account their respective rights and obligations in the context of this Regulation, to make an informed deployment
of AI systems, as well as to gain awareness about the opportunities and risks of AI and possible harm it can cause;

ELI: http://data.europa.eu/eli/reg/2024/1689/oj

49/144


EN

OJ L, 12.7.2024

(57) ‘testing in real-world conditions’ means the temporary testing of an AI system for its intended purpose in real-world
conditions outside a laboratory or otherwise simulated environment, with a view to gathering reliable and robust data
and to assessing and verifying the conformity of the AI system with the requirements of this Regulation and it does
not qualify as placing the AI system on the market or putting it into service within the meaning of this Regulation,
provided that all the conditions laid down in Article 57 or 60 are fulfilled;

(58) ‘subject’, for the purpose of real-world testing, means a natural person who participates in testing in real-world

conditions;

(59) ‘informed consent’ means a subject’s freely given, specific, unambiguous and voluntary expression of his or her
willingness to participate in a particular testing in real-world conditions, after having been informed of all aspects of
the testing that are relevant to the subject’s decision to participate;

(60) ‘deep fake’ means AI-generated or manipulated image, audio or video content that resembles existing persons, objects,

places, entities or events and would falsely appear to a person to be authentic or truthful;

(61) ‘widespread infringement’ means any act or omission contrary to Union law protecting the interest of individuals,

which:

(a) has harmed or is likely to harm the collective interests of individuals residing in at least two Member States other

than the Member State in which:

(i) the act or omission originated or took place;

(ii) the provider concerned, or, where applicable, its authorised representative is located or established; or

(iii) the deployer is established, when the infringement is committed by the deployer;

(b) has caused, causes or is likely to cause harm to the collective interests of individuals and has common features,
including the same unlawful practice or the same interest being infringed, and is occurring concurrently,
committed by the same operator, in at least three Member States;

(62) ‘critical infrastructure’ means critical infrastructure as defined in Article 2, point (4), of Directive (EU) 2022/2557;

(63) ‘general-purpose AI model’ means an AI model, including where such an AI model is trained with a large amount of
data using self-supervision at scale, that displays significant generality and is capable of competently performing
a wide range of distinct tasks regardless of the way the model is placed on the market and that can be integrated into
a variety of downstream systems or applications, except AI models that are used for research, development or
prototyping activities before they are placed on the market;

(64) ‘high-impact capabilities’ means capabilities that match or exceed the capabilities recorded in the most advanced

general-purpose AI models;

(65) ‘systemic risk’ means a risk that is specific to the high-impact capabilities of general-purpose AI models, having
a significant impact on the Union market due to their reach, or due to actual or reasonably foreseeable negative effects
on public health, safety, public security, fundamental rights, or the society as a whole, that can be propagated at scale
across the value chain;

(66) ‘general-purpose AI system’ means an AI system which is based on a general-purpose AI model and which has the

capability to serve a variety of purposes, both for direct use as well as for integration in other AI systems;

(67) ‘floating-point operation’ means any mathematical operation or assignment involving floating-point numbers, which
are a subset of the real numbers typically represented on computers by an integer of fixed precision scaled by an
integer exponent of a fixed base;

(68) ‘downstream provider’ means a provider of an AI system, including a general-purpose AI system, which integrates an
AI model, regardless of whether the AI model is provided by themselves and vertically integrated or provided by
another entity based on contractual relations.

50/144

ELI: http://data.europa.eu/eli/reg/2024/1689/oj


OJ L, 12.7.2024

EN


---

## Article 12

<!-- verbatim, lines 4328-4362 of the official English text -->

Article 12

Record-keeping

High-risk AI systems shall technically allow for the automatic recording of events (logs) over the lifetime of the

1.
system.

In order to ensure a level of traceability of the functioning of a high-risk AI system that is appropriate to the intended

2.
purpose of the system, logging capabilities shall enable the recording of events relevant for:

(a)

identifying situations that may result in the high-risk AI system presenting a risk within the meaning of Article 79(1) or
in a substantial modification;

(b) facilitating the post-market monitoring referred to in Article 72; and

(c) monitoring the operation of high-risk AI systems referred to in Article 26(5).

3.

For high-risk AI systems referred to in point 1 (a), of Annex III, the logging capabilities shall provide, at a minimum:

(a) recording of the period of each use of the system (start date and time and end date and time of each use);

(b) the reference database against which input data has been checked by the system;

(c) the input data for which the search has led to a match;

(d) the identification of the natural persons involved in the verification of the results, as referred to in Article 14(5).


---

## Article 14

<!-- verbatim, lines 4436-4506 of the official English text -->

Article 14

Human oversight

High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine

1.
interface tools, that they can be effectively overseen by natural persons during the period in which they are in use.

Human oversight shall aim to prevent or minimise the risks to health, safety or fundamental rights that may emerge
2.
when a high-risk AI system is used in accordance with its intended purpose or under conditions of reasonably foreseeable
misuse, in particular where such risks persist despite the application of other requirements set out in this Section.

The oversight measures shall be commensurate with the risks, level of autonomy and context of use of the high-risk

3.
AI system, and shall be ensured through either one or both of the following types of measures:

(a) measures identified and built, when technically feasible, into the high-risk AI system by the provider before it is placed

on the market or put into service;

(b) measures identified by the provider before placing the high-risk AI system on the market or putting it into service and

that are appropriate to be implemented by the deployer.

For the purpose of implementing paragraphs 1, 2 and 3, the high-risk AI system shall be provided to the deployer in

4.
such a way that natural persons to whom human oversight is assigned are enabled, as appropriate and proportionate:

(a) to properly understand the relevant capacities and limitations of the high-risk AI system and be able to duly monitor its

operation, including in view of detecting and addressing anomalies, dysfunctions and unexpected performance;

(b) to remain aware of the possible tendency of automatically relying or over-relying on the output produced by a high-risk
AI system (automation bias), in particular for high-risk AI systems used to provide information or recommendations for
decisions to be taken by natural persons;

(c) to correctly interpret the high-risk AI system’s output, taking into account, for example, the interpretation tools and

methods available;

60/144

ELI: http://data.europa.eu/eli/reg/2024/1689/oj


OJ L, 12.7.2024

EN

(d) to decide, in any particular situation, not to use the high-risk AI system or to otherwise disregard, override or reverse

the output of the high-risk AI system;

(e) to intervene in the operation of the high-risk AI system or interrupt the system through a ‘stop’ button or a similar

procedure that allows the system to come to a halt in a safe state.

5.
For high-risk AI systems referred to in point 1(a) of Annex III, the measures referred to in paragraph 3 of this Article
shall be such as to ensure that, in addition, no action or decision is taken by the deployer on the basis of the identification
resulting from the system unless that identification has been separately verified and confirmed by at least two natural
persons with the necessary competence, training and authority.

The requirement for a separate verification by at least two natural persons shall not apply to high-risk AI systems used for
the purposes of law enforcement, migration, border control or asylum, where Union or national law considers the
application of this requirement to be disproportionate.


---

## Article 25

<!-- verbatim, lines 4962-5023 of the official English text -->

Article 25

Responsibilities along the AI value chain

Any distributor, importer, deployer or other third-party shall be considered to be a provider of a high-risk AI system
1.
for the purposes of this Regulation and shall be subject to the obligations of the provider under Article 16, in any of the
following circumstances:

(a) they put their name or trademark on a high-risk AI system already placed on the market or put into service, without

prejudice to contractual arrangements stipulating that the obligations are otherwise allocated;

(b) they make a substantial modification to a high-risk AI system that has already been placed on the market or has already

been put into service in such a way that it remains a high-risk AI system pursuant to Article 6;

(c) they modify the intended purpose of an AI system, including a general-purpose AI system, which has not been classified
as high-risk and has already been placed on the market or put into service in such a way that the AI system concerned
becomes a high-risk AI system in accordance with Article 6.

2. Where the circumstances referred to in paragraph 1 occur, the provider that initially placed the AI system on the
market or put it into service shall no longer be considered to be a provider of that specific AI system for the purposes of
this Regulation. That initial provider shall closely cooperate with new providers and shall make available the necessary
information and provide the reasonably expected technical access and other assistance that are required for the fulfilment of
the obligations set out in this Regulation, in particular regarding the compliance with the conformity assessment of
high-risk AI systems. This paragraph shall not apply in cases where the initial provider has clearly specified that its AI
system is not to be changed into a high-risk AI system and therefore does not fall under the obligation to hand over the
documentation.

3.
In the case of high-risk AI systems that are safety components of products covered by the Union harmonisation
legislation listed in Section A of Annex I, the product manufacturer shall be considered to be the provider of the high-risk
AI system, and shall be subject to the obligations under Article 16 under either of the following circumstances:

(a) the high-risk AI system is placed on the market together with the product under the name or trademark of the product

manufacturer;

(b) the high-risk AI system is put into service under the name or trademark of the product manufacturer after the product

has been placed on the market.

The provider of a high-risk AI system and the third party that supplies an AI system, tools, services, components, or
4.
processes that are used or integrated in a high-risk AI system shall, by written agreement, specify the necessary information,
capabilities, technical access and other assistance based on the generally acknowledged state of the art, in order to enable
the provider of the high-risk AI system to fully comply with the obligations set out in this Regulation. This paragraph shall
not apply to third parties making accessible to the public tools, services, processes, or components, other than
general-purpose AI models, under a free and open-source licence.

The AI Office may develop and recommend voluntary model terms for contracts between providers of high-risk AI systems
and third parties that supply tools, services, components or processes that are used for or integrated into high-risk AI
systems. When developing those voluntary model terms, the AI Office shall take into account possible contractual
requirements applicable in specific sectors or business cases. The voluntary model terms shall be published and be available
free of charge in an easily usable electronic format.

Paragraphs 2 and 3 are without prejudice to the need to observe and protect intellectual property rights, confidential

5.
business information and trade secrets in accordance with Union and national law.


---

## Article 26

<!-- verbatim, lines 5024-5150 of the official English text -->

Article 26

Obligations of deployers of high-risk AI systems

Deployers of high-risk AI systems shall take appropriate technical and organisational measures to ensure they use

1.
such systems in accordance with the instructions for use accompanying the systems, pursuant to paragraphs 3 and 6.

ELI: http://data.europa.eu/eli/reg/2024/1689/oj

67/144


EN

OJ L, 12.7.2024

Deployers shall assign human oversight to natural persons who have the necessary competence, training and

2.
authority, as well as the necessary support.

3.
The obligations set out in paragraphs 1 and 2, are without prejudice to other deployer obligations under Union or
national law and to the deployer’s freedom to organise its own resources and activities for the purpose of implementing the
human oversight measures indicated by the provider.

4. Without prejudice to paragraphs 1 and 2, to the extent the deployer exercises control over the input data, that
deployer shall ensure that input data is relevant and sufficiently representative in view of the intended purpose of the
high-risk AI system.

5.
Deployers shall monitor the operation of the high-risk AI system on the basis of the instructions for use and, where
relevant, inform providers in accordance with Article 72. Where deployers have reason to consider that the use of the
high-risk AI system in accordance with the instructions may result in that AI system presenting a risk within the meaning of
Article 79(1), they shall, without undue delay, inform the provider or distributor and the relevant market surveillance
authority, and shall suspend the use of that system. Where deployers have identified a serious incident, they shall also
immediately inform first the provider, and then the importer or distributor and the relevant market surveillance authorities
of that incident. If the deployer is not able to reach the provider, Article 73 shall apply mutatis mutandis. This obligation
shall not cover sensitive operational data of deployers of AI systems which are law enforcement authorities.

For deployers that are financial institutions subject to requirements regarding their internal governance, arrangements or
processes under Union financial services law, the monitoring obligation set out in the first subparagraph shall be deemed to
be fulfilled by complying with the rules on internal governance arrangements, processes and mechanisms pursuant to the
relevant financial service law.

6.
Deployers of high-risk AI systems shall keep the logs automatically generated by that high-risk AI system to the extent
such logs are under their control, for a period appropriate to the intended purpose of the high-risk AI system, of at least six
months, unless provided otherwise in applicable Union or national law, in particular in Union law on the protection of
personal data.

Deployers that are financial institutions subject to requirements regarding their internal governance, arrangements or
processes under Union financial services law shall maintain the logs as part of the documentation kept pursuant to the
relevant Union financial service law.

7.
Before putting into service or using a high-risk AI system at the workplace, deployers who are employers shall inform
workers’ representatives and the affected workers that they will be subject to the use of the high-risk AI system. This
information shall be provided, where applicable, in accordance with the rules and procedures laid down in Union and
national law and practice on information of workers and their representatives.

8.
Deployers of high-risk AI systems that are public authorities, or Union institutions, bodies, offices or agencies shall
comply with the registration obligations referred to in Article 49. When such deployers find that the high-risk AI system
that they envisage using has not been registered in the EU database referred to in Article 71, they shall not use that system
and shall inform the provider or the distributor.

9. Where applicable, deployers of high-risk AI systems shall use the information provided under Article 13 of this
Regulation to comply with their obligation to carry out a data protection impact assessment under Article 35 of Regulation
(EU) 2016/679 or Article 27 of Directive (EU) 2016/680.

10. Without prejudice to Directive (EU) 2016/680, in the framework of an investigation for the targeted search of
a person suspected or convicted of having committed a criminal offence, the deployer of a high-risk AI system for
post-remote biometric identification shall request an authorisation, ex ante, or without undue delay and no later than 48
hours, by a judicial authority or an administrative authority whose decision is binding and subject to judicial review, for the
use of that system, except when it is used for the initial identification of a potential suspect based on objective and verifiable
facts directly linked to the offence. Each use shall be limited to what is strictly necessary for the investigation of a specific
criminal offence.

If the authorisation requested pursuant to the first subparagraph is rejected, the use of the post-remote biometric
identification system linked to that requested authorisation shall be stopped with immediate effect and the personal data
linked to the use of the high-risk AI system for which the authorisation was requested shall be deleted.

68/144

ELI: http://data.europa.eu/eli/reg/2024/1689/oj


OJ L, 12.7.2024

EN

In no case shall such high-risk AI system for post-remote biometric identification be used for law enforcement purposes in
an untargeted way, without any link to a criminal offence, a criminal proceeding, a genuine and present or genuine and
foreseeable threat of a criminal offence, or the search for a specific missing person. It shall be ensured that no decision that
produces an adverse legal effect on a person may be taken by the law enforcement authorities based solely on the output of
such post-remote biometric identification systems.

This paragraph is without prejudice to Article 9 of Regulation (EU) 2016/679 and Article 10 of Directive (EU) 2016/680
for the processing of biometric data.

Regardless of the purpose or deployer, each use of such high-risk AI systems shall be documented in the relevant police file
and shall be made available to the relevant market surveillance authority and the national data protection authority upon
request, excluding the disclosure of sensitive operational data related to law enforcement. This subparagraph shall be
without prejudice to the powers conferred by Directive (EU) 2016/680 on supervisory authorities.

Deployers shall submit annual reports to the relevant market surveillance and national data protection authorities on their
use of post-remote biometric identification systems, excluding the disclosure of sensitive operational data related to law
enforcement. The reports may be aggregated to cover more than one deployment.

Member States may introduce, in accordance with Union law, more restrictive laws on the use of post-remote biometric
identification systems.

11. Without prejudice to Article 50 of this Regulation, deployers of high-risk AI systems referred to in Annex III that
make decisions or assist in making decisions related to natural persons shall inform the natural persons that they are subject
to the use of the high-risk AI system. For high-risk AI systems used for law enforcement purposes Article 13 of Directive
(EU) 2016/680 shall apply.

Deployers shall cooperate with the relevant competent authorities in any action those authorities take in relation to

12.
the high-risk AI system in order to implement this Regulation.

Fundamental rights impact assessment for high-risk AI systems


---

## Article 50

<!-- verbatim, lines 6123-6199 of the official English text -->

Article 50

1.
Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in
such a way that the natural persons concerned are informed that they are interacting with an AI system, unless this is
obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect, taking
into account the circumstances and the context of use. This obligation shall not apply to AI systems authorised by law to
detect, prevent, investigate or prosecute criminal offences, subject to appropriate safeguards for the rights and freedoms of
third parties, unless those systems are available for the public to report a criminal offence.

2.
Providers of AI systems, including general-purpose AI systems, generating synthetic audio, image, video or text
content, shall ensure that the outputs of the AI system are marked in a machine-readable format and detectable as
artificially generated or manipulated. Providers shall ensure their technical solutions are effective, interoperable, robust and
reliable as far as this is technically feasible, taking into account the specificities and limitations of various types of content,
the costs of implementation and the generally acknowledged state of the art, as may be reflected in relevant technical
standards. This obligation shall not apply to the extent the AI systems perform an assistive function for standard editing or
do not substantially alter the input data provided by the deployer or the semantics thereof, or where authorised by law to
detect, prevent, investigate or prosecute criminal offences.

3.
Deployers of an emotion recognition system or a biometric categorisation system shall inform the natural persons
exposed thereto of the operation of the system, and shall process the personal data in accordance with Regulations (EU)
2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, as applicable. This obligation shall not apply to AI systems
used for biometric categorisation and emotion recognition, which are permitted by law to detect, prevent or investigate
criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, and in accordance with
Union law.

4.
Deployers of an AI system that generates or manipulates image, audio or video content constituting a deep fake, shall
disclose that the content has been artificially generated or manipulated. This obligation shall not apply where the use is
authorised by law to detect, prevent, investigate or prosecute criminal offence. Where the content forms part of an evidently
artistic, creative, satirical, fictional or analogous work or programme, the transparency obligations set out in this paragraph
are limited to disclosure of the existence of such generated or manipulated content in an appropriate manner that does not
hamper the display or enjoyment of the work.

Deployers of an AI system that generates or manipulates text which is published with the purpose of informing the public
on matters of public interest shall disclose that the text has been artificially generated or manipulated. This obligation shall
not apply where the use is authorised by law to detect, prevent, investigate or prosecute criminal offences or where the
AI-generated content has undergone a process of human review or editorial control and where a natural or legal person
holds editorial responsibility for the publication of the content.

82/144

ELI: http://data.europa.eu/eli/reg/2024/1689/oj


OJ L, 12.7.2024

EN

The information referred to in paragraphs 1 to 4 shall be provided to the natural persons concerned in a clear and
5.
distinguishable manner at the latest at the time of the first interaction or exposure. The information shall conform to the
applicable accessibility requirements.

Paragraphs 1 to 4 shall not affect the requirements and obligations set out in Chapter III, and shall be without

6.
prejudice to other transparency obligations laid down in Union or national law for deployers of AI systems.

7.
The AI Office shall encourage and facilitate the drawing up of codes of practice at Union level to facilitate the effective
implementation of the obligations regarding the detection and labelling of artificially generated or manipulated content.
The Commission may adopt implementing acts to approve those codes of practice in accordance with the procedure laid
down in Article 56 (6). If it deems the code is not adequate, the Commission may adopt an implementing act specifying
common rules for the implementation of those obligations in accordance with the examination procedure laid down in
Article 98(2).

CHAPTER V

GENERAL-PURPOSE AI MODELS

SECTION 1

Classification rules


---

## Article 72

<!-- verbatim, lines 7596-7634 of the official English text -->

Article 72

Post-market monitoring by providers and post-market monitoring plan for high-risk AI systems

Providers shall establish and document a post-market monitoring system in a manner that is proportionate to the

1.
nature of the AI technologies and the risks of the high-risk AI system.

2.
The post-market monitoring system shall actively and systematically collect, document and analyse relevant data
which may be provided by deployers or which may be collected through other sources on the performance of high-risk AI
systems throughout their lifetime, and which allow the provider to evaluate the continuous compliance of AI systems with
the requirements set out in Chapter III, Section 2. Where relevant, post-market monitoring shall include an analysis of the
interaction with other AI systems. This obligation shall not cover sensitive operational data of deployers which are
law-enforcement authorities.

3.
The post-market monitoring system shall be based on a post-market monitoring plan. The post-market monitoring
plan shall be part of the technical documentation referred to in Annex IV. The Commission shall adopt an implementing act
laying down detailed provisions establishing a template for the post-market monitoring plan and the list of elements to be
included in the plan by 2 February 2026. That implementing act shall be adopted in accordance with the examination
procedure referred to in Article 98(2).

For high-risk AI systems covered by the Union harmonisation legislation listed in Section A of Annex I, where
4.
a post-market monitoring system and plan are already established under that legislation, in order to ensure consistency,
avoid duplications and minimise additional burdens, providers shall have a choice of integrating, as appropriate, the
necessary elements described in paragraphs 1, 2 and 3 using the template referred in paragraph 3 into systems and plans
already existing under that legislation, provided that it achieves an equivalent level of protection.

The first subparagraph of this paragraph shall also apply to high-risk AI systems referred to in point 5 of Annex III placed
on the market or put into service by financial institutions that are subject to requirements under Union financial services
law regarding their internal governance, arrangements or processes.

SECTION 2

Sharing of information on serious incidents


---

## Annex III

<!-- verbatim, lines 9567-9734 of the official English text -->

ANNEX III

High-risk AI systems referred to in Article 6(2)

High-risk AI systems pursuant to Article 6(2) are the AI systems listed in any of the following areas:

1.

Biometrics, in so far as their use is permitted under relevant Union or national law:

(a) remote biometric identification systems.

This shall not include AI systems intended to be used for biometric verification the sole purpose of which is to
confirm that a specific natural person is the person he or she claims to be;

(b) AI systems intended to be used for biometric categorisation, according to sensitive or protected attributes or

characteristics based on the inference of those attributes or characteristics;

(c) AI systems intended to be used for emotion recognition.

2.

Critical infrastructure: AI systems intended to be used as safety components in the management and operation of
critical digital infrastructure, road traffic, or in the supply of water, gas, heating or electricity.

3.

Education and vocational training:

(a) AI systems intended to be used to determine access or admission or to assign natural persons to educational and

vocational training institutions at all levels;

(b) AI systems intended to be used to evaluate learning outcomes, including when those outcomes are used to steer

the learning process of natural persons in educational and vocational training institutions at all levels;

(c) AI systems intended to be used for the purpose of assessing the appropriate level of education that an individual
will receive or will be able to access, in the context of or within educational and vocational training institutions
at all levels;

(d) AI systems intended to be used for monitoring and detecting prohibited behaviour of students during tests in the

context of or within educational and vocational training institutions at all levels.

4.

Employment, workers’ management and access to self-employment:

(a) AI systems intended to be used for the recruitment or selection of natural persons, in particular to place targeted

job advertisements, to analyse and filter job applications, and to evaluate candidates;

(b) AI systems intended to be used to make decisions affecting terms of work-related relationships, the promotion or
termination of work-related contractual relationships, to allocate tasks based on individual behaviour or personal
traits or characteristics or to monitor and evaluate the performance and behaviour of persons in such
relationships.

5.

Access to and enjoyment of essential private services and essential public services and benefits:

(a) AI systems intended to be used by public authorities or on behalf of public authorities to evaluate the eligibility
of natural persons for essential public assistance benefits and services, including healthcare services, as well as to
grant, reduce, revoke, or reclaim such benefits and services;

(b) AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score,

with the exception of AI systems used for the purpose of detecting financial fraud;

(c) AI systems intended to be used for risk assessment and pricing in relation to natural persons in the case of life

and health insurance;

ELI: http://data.europa.eu/eli/reg/2024/1689/oj

127/144


EN

OJ L, 12.7.2024

(d) AI systems intended to evaluate and classify emergency calls by natural persons or to be used to dispatch, or to
establish priority in the dispatching of, emergency first response services, including by police, firefighters and
medical aid, as well as of emergency healthcare patient triage systems.

6.

Law enforcement, in so far as their use is permitted under relevant Union or national law:

(a) AI systems intended to be used by or on behalf of law enforcement authorities, or by Union institutions, bodies,
offices or agencies in support of law enforcement authorities or on their behalf to assess the risk of a natural
person becoming the victim of criminal offences;

(b) AI systems intended to be used by or on behalf of law enforcement authorities or by Union institutions, bodies,

offices or agencies in support of law enforcement authorities as polygraphs or similar tools;

(c) AI systems intended to be used by or on behalf of law enforcement authorities, or by Union institutions, bodies,
offices or agencies, in support of law enforcement authorities to evaluate the reliability of evidence in the course
of the investigation or prosecution of criminal offences;

(d) AI systems intended to be used by law enforcement authorities or on their behalf or by Union institutions,
bodies, offices or agencies in support of law enforcement authorities for assessing the risk of a natural person
offending or re-offending not solely on the basis of the profiling of natural persons as referred to in Article 3(4)
of Directive (EU) 2016/680, or to assess personality traits and characteristics or past criminal behaviour of
natural persons or groups;

(e) AI systems intended to be used by or on behalf of law enforcement authorities or by Union institutions, bodies,
offices or agencies in support of law enforcement authorities for the profiling of natural persons as referred to in
Article 3(4) of Directive (EU) 2016/680 in the course of the detection, investigation or prosecution of criminal
offences.

7.

Migration, asylum and border control management, in so far as their use is permitted under relevant Union or
national law:

(a) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies,

offices or agencies as polygraphs or similar tools;

(b) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies,
offices or agencies to assess a risk, including a security risk, a risk of irregular migration, or a health risk, posed
by a natural person who intends to enter or who has entered into the territory of a Member State;

(c) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies,
offices or agencies to assist competent public authorities for the examination of applications for asylum, visa or
residence permits and for associated complaints with regard to the eligibility of the natural persons applying for
a status, including related assessments of the reliability of evidence;

(d) AI systems intended to be used by or on behalf of competent public authorities, or by Union institutions, bodies,
offices or agencies, in the context of migration, asylum or border control management, for the purpose of
detecting, recognising or identifying natural persons, with the exception of the verification of travel documents.

8.

Administration of justice and democratic processes:

(a) AI systems intended to be used by a judicial authority or on their behalf to assist a judicial authority in
researching and interpreting facts and the law and in applying the law to a concrete set of facts, or to be used in
a similar way in alternative dispute resolution;

128/144

ELI: http://data.europa.eu/eli/reg/2024/1689/oj


OJ L, 12.7.2024

EN

(b) AI systems intended to be used for influencing the outcome of an election or referendum or the voting
behaviour of natural persons in the exercise of their vote in elections or referenda. This does not include AI
systems to the output of which natural persons are not directly exposed, such as tools used to organise, optimise
or structure political campaigns from an administrative or logistical point of view.

ELI: http://data.europa.eu/eli/reg/2024/1689/oj

129/144


EN

OJ L, 12.7.2024


---
