# Larsen et al. - 2025 - Validity in Design Science

_Source: Larsen et al. - 2025 - Validity in Design Science.pdf_

METHODS ARTICLE
V D S 1
ALIDITY IN ESIGN CIENCE
Kai R. Larsen
Leeds School of Business, University of Colorado Boulder,
Boulder, CO, U.S.A. {kai.larsen@colorado.edu}
Roman Lukyanenko
McIntire School of Commerce, University of Virginia
Charlottesville, VA, U.S.A. {romanl@virginia.edu}
Roland M. Mueller
Department of Business and Economics, Berlin School of Economics and Law
Berlin, GERMANY {roland.mueller@hwr-berlin.de}
Veda C. Storey
J. Mack Robinson College of Business, Georgia State University
Atlanta, GA, U.S.A. {vstorey@gsu.edu}
Jeffrey Parsons
Faculty of Business Administration, Memorial University of Newfoundland
St. John’s, NL, CANADA {jeffreyp@mun.ca}
Debra VanderMeer
College of Business, Florida International University
Miami, Florida, U.S.A. {vanderd@fiu.edu}
Dirk S. Hovorka
University of Sydney Business School, University of Sydney
Sydney, AUSTRALIA {dirk.hovorka@sydney.edu.au}
Researchers must ensure that the claims about the knowledge produced by their work are valid. However,
validity is neither well-understood nor consistently established in design science, which involves the
development and evaluation of artifacts (models, methods, instantiations, and theories) to solve problems.
As a result, it is challenging to demonstrate and communicate the validity of knowledge claims about
artifacts. This paper defines validity in design science and derives a “design science validity framework”
and a process model for applying it. The framework comprises three high-level claim and validity types—
criterion, causal, and context—as well as validity subtypes. The framework guides researchers in integrating
validity considerations into projects employing design science and contributes to the growing body of
research on design science methodology. It also provides a systematic way to articulate and validate the
knowledge claims of design science projects. We apply the framework to examples from existing research
and then use it to demonstrate the validity of knowledge claims about the framework itself.
Keywords: Design science, design science research (DSR), design science validity framework, knowledge
claim, research validity, criterion validity, causal validity, context validity, characteristic validity, efficacy
validity, external validity, ecological validity, evaluation, validation
1 Balaji Padmanabhan was the accepting senior editor for this paper. Stefan Seidel served as the associate editor. The transparency materials for this paper are
available at https://osf.io/ca6vg/.
©2025. The Authors. This work is licensed under the terms of the Creative Commons Attribution CC BY-NC-ND 4.0 License
(https://creativecommons.org/licenses/by-nc-nd/4.0/)
DOI:10.25300/MISQ/2024/18064 MIS Quarterly Vol. 49 No. 4 pp. 1267-1294 / December 2025 1267
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Introduction such as applicability checks (Rosemann & Vessey, 2008),
respond to multiple (often unstated) claims, leading to questions
regarding what exactly has been validated. Despite the potential
Scientific knowledge must be credible and dependable (Burton-
benefits, there have been no systematic attempts to define or
Jones et al., 2021; Creswell & Miller, 2000). An established
survey validity across all the artifact types addressed by design
validity tradition facilitates this because it provides a systematic
scientists (e.g., models, methods, design theories; see Gregor &
way of evaluating the claimed contributions to knowledge in
Hevner, 2013) or provide a process for validating claims.
research studies (Cook & Campbell, 1979; Guba & Lincoln,
Hence, the essential question of what constitutes validity in
1994). Each scientific discipline has patterns and procedures to
design science remains unanswered.
evaluate the validity of knowledge claims regarding phenomena
of interest. Articulating these patterns provides evaluative
A systematic approach to validity will benefit design science.
clarity, increases research efficiency, promotes the sharing of
First, it will promote high-quality scholarship. Critical to the
best practices, facilitates cumulative science, and contributes to
quality of design science is the link between knowledge claims
greater public trust in science.
and the evidence that supports these claims. This can be
facilitated by following evaluation procedures in accordance
In design science—a genre of research in information systems,
with agreed-upon structures known to support the types of
computer science, engineering, medicine, management, and
claims made. These procedures commonly demand procedural
material and biomedical sciences—researchers advance
rigor and careful argumentation (e.g., evidence of causality for
knowledge claims about the characteristics or performance of
internal validity, often provided through randomized
the artifacts they invent. Researchers have proposed processes
experiments). Establishing validity would make the linkage
for conducting design science, each of which identifies
between claims and their validation more explicit and more
evaluation as an essential step (Gregor & Hevner, 2013; Hevner
amenable to attention and scrutiny. This transparency is
et al., 2004; Peffers et al., 2008; Prat et al., 2015; Sein et al.,
important for engendering trust and confidence in the claims
2011). However, existing methods and frameworks neither
and reported findings (Burton-Jones et al., 2021).
consider the validity of knowledge claims to be a core
component of artifact evaluation nor agree on what it means to
Second, as specific types of validity address specific types of
assess the validity of knowledge claims about artifacts.
claims (e.g., internal validity addresses claims of causation),
establishing a validity tradition for design science will lead to
Design science exhibits recurring patterns of knowledge claims.
making knowledge claims more explicit. This can help
Examples include: the artifact outperforms the state of the art
researchers better appreciate and communicate the
(Padmanabhan et al., 2022), a recent version of the artifact
contributions they are making and facilitate the validation
performs better than the previous version(s) (Sein et al., 2011),
process. Furthermore, the explicated knowledge claims can also
the model corresponds to a referent real-world system
be used by other researchers seeking to extend the original
(Gonzalez-Huerta et al., 2017), and the artifact works due to the
contributions both within and beyond design science, thus
presence of particular design features (Abbasi et al., 2012).
allowing design scientists to better contribute to a cumulative
There is also a repertoire of common evaluation approaches in
tradition of research on the design, use, and impact of
design science (Prat et al., 2015; Venable et al., 2016), although
information technology artifacts.
these do not address the logic that connects claims to validation,
the process of establishing the validity of a particular type of Third, a comprehensive conceptualization of validity will
knowledge claim. increase the impact of design science on the real world. By
sensitizing researchers to the nature of knowledge claims and
While validity types are used in some design science projects, validity types, artifacts that fail to serve their intended purpose
these are generally adapted from other traditions. For example, when exposed to unexpected real-world circumstances become
internal and external validity are adapted from psychometrics less likely. For example, in machine learning, it is important for
(Baskerville et al., 2015; vom Brocke, Hevner, et al., 2020), researchers to be aware of which artifact features produced the
whereas validity metrics, such as precision and recall, are taken improved outcomes. Still, these are narrowly focused on the
from information retrieval, statistics, and other disciplines performance of a proposed artifact. A more inclusive
(Larsen & Becker, 2020). An exception is instantiation validity conception of validity would consider an artifact’s applicability
(Lukyanenko & Parsons, 2020), which was proposed as a native for varied real-world conditions, including for broader tasks and
design science validity type. different user groups (Ethayarajh & Jurafsky, 2020).
Most design science validations lack any label, making it Fourth, establishing a validity tradition will facilitate the
difficult to reference them effectively and share best practices publication of design science studies. As a reflection of
with the community. Furthermore, some evaluation procedures, community norms and shared concepts, a validity tradition
1268 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
boosts research productivity by increasing validation extensive analysis of research on validity, and a comprehensive
consistency (Chan, 2014) and streamlining validation practices. analysis of design science evaluation, we demonstrate the utility
Note that the prolific fields of econometrics and psychometrics of our framework for researchers, its ability to capture existing
have distinct validity or validation approaches (Taylor, 2013), validation practices, and its parsimony. We conclude with a
as do qualitative research (Creswell & Miller, 2000) and areas general discussion on the nature and importance of design
of computer science and software engineering, such as model science validity, recommend how the framework can be used,
simulation (e.g., Pääkkönen et al., 2017) and problem and identify future research opportunities.
decidability (e.g., Fan et al., 2018). Across disciplines, a higher
level of agreement on core disciplinary norms (including Methodological Developments in Design
validation) correlates with increased research productivity and
Science
publication quality (Gumport, 2007). The formalization of
shared disciplinary conceptualizations is vital to accelerating
Design science has developed methodological foundations to
scientific progress (National Academies, 2022).
facilitate credible and dependable practical scientific
knowledge. These efforts have focused on ensuring rigor in
Finally, establishing the nature of validity in design science will
artifact development and evaluating the utility and quality of
position it with respect to established traditions (e.g., in the
the artifacts and design knowledge (see Table 1 for specific
behavioral sciences) and better communicate the distinct
topics pursued). Whereas rigor in artifact development has
contributions of design science to outsiders. The common
received much attention, rigor in evaluating the utility and
patterns of validation receive a systematic name, thereby
quality of artifacts and design knowledge has lagged, even
helping design science scholars and outsiders reference these
though this is a major challenge.
evaluation approaches. This, in turn, helps to establish design
science identity.
A significant step toward establishing rigor for design science
is understanding what evaluations already exist, how they
This research makes several contributions. We first examine
how validity concepts have been used in design science. We provide complementary knowledge, and how they overlap.
then consider the general nature of validity to identify the No previous work has attempted to understand the rigor of
established foundations that could benefit design scientists. We design science evaluation by establishing the possible types of
do so by developing insights into the logic and relationships validities. Doing so requires understanding types of
among the claims, artifact types, validity types, and evaluation knowledge claims, artifacts, and validation approaches.
context. These foundations then allow us to define validity
types and use them appropriately to evaluate design science We reviewed prominent design science framework journal
knowledge claims. articles as summarized in Table 2. Most frameworks in Table
2 deal primarily with the rigor of artifact development. For
Next, we develop the design science validity framework to example, Sein et al. (2011) focused on action design research
provide a systematic way to articulate and validate the (ADR), where evaluations occur in a real-world, authentic
knowledge claims of design science projects. The framework context. Venable et al. (2016) distinguished between
comprises three high-level knowledge claim and validity formative and summative evaluations, focusing on when
types—criterion, causal, and context—as well as validity evaluations are conducted. Gregor and Hevner (2013)
subtypes. This structure corresponds to the aim of design considered ways to position and present design science and
science to develop innovative artifacts as solutions to societal whether evaluations occur inside or outside a development
challenges, while contributing scientific knowledge that context. Prat et al. (2015) organized evaluation approaches
practitioners can reuse in diverse contexts. The framework is into a taxonomy of five dimensions of distinct evaluation
inclusive in its coverage of design science artifacts, including types. Baskerville et al. (2015) developed a framework to
implemented systems (e.g., tools and deployed instantiations), highlight the different types of knowledge production that can
abstract contributions that encapsulate blueprints for systems occur throughout a design science project. Tuunanen et al.
development (e.g., conceptual models or machine learning (2024) provided an approach for managing complex,
methods), and theoretical design knowledge (e.g., design multistage projects by suggesting that these stages
theories that prescribe design and action to attain specific goals, (“echelons”) produce different artifacts that can be evaluated
see Gregor & Jones, 2007). at each stage. It is noteworthy that validity concerns have
grown over time from little to no consideration in early
Finally, we evaluate the design science validity framework frameworks (e.g., Hevner et al., 2004; Peffers et al., 2008) to
through a series of studies informed recursively by the active consideration in recent methodological studies (e.g.,
framework itself. Through two applicability checks, an Baskerville et al., 2015; Tuunanen et al., 2024).
MIS Quarterly Vol. 49 No. 4 / December 2025 1269
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Table 1. Methodological Foundations in Design Science
Contribution Reference
Integration of systems development with
Nunamaker et al. (1991); March and Smith (1995)
rigorous theory and empirical evaluation
Approaches to evaluating artifacts and Hevner et al. (2004); Venable et al. (2016); Prat et al. (2015); Gregor and
theories Jones (2007); Tuunanen et al. (2024)
Peffers et al. (2008); Gregor and Hevner (2013); Johannesson and Perjons
Methods to produce and communicate
(2014); Baskerville et al. (2015); Avdiji and Winter (2019); Iivari (2015);
design science
Gregor et al. (2020); Tuunanen et al. (2024)
Arazy et al. (2010); Gregor and Jones (2007); Kuechler and Vaishnavi
Alignment of kernel theories with artifacts
(2012); vom Brocke et al. (2020)
vom Brocke et al. (2021); Burton-Jones et al. (2021); Lukyanenko and
Transparency
Parsons (2020); Hevner et al. (2024)
Alignment with practice Sein et al. (2011); Lukyanenko and Parsons (2020); Hevner et al. (2024)
Mandviwalla (2015); Gregor and Jones (2007); Gregory and Muntermann
Design theorization
(2014); Lukyanenko and Parsons (2020); Gregor et al. (2020)
Table 2. Design Science Frameworks and the Role of Validity
Paper Framework overview Validity and claims Evaluation
Hevner et Design science consists Minimal emphasis on Proposes two fundamental questions that require
al. (2004) of building and evaluating validity. Cites other work evidence from evaluations: (1) What utility does
artifacts and connecting on how the accumulation of the artifact provide? (2) How is that utility
them to the environment evidence will eventually demonstrated? Proposes that contribution arises
and design knowledge establish the validity of from utility demonstrated through evaluation.
base. broader design science
claims.
Peffers et al. A six-step iterative Little emphasis on validity. Researchers observe and measure how well the
(2008) process for presenting Suggests that design artifact supports a solution. Involves comparing
and evaluating design science has had to employ objectives of a solution to actual observed results
science. “ad hoc arguments” (p. 50). from using an artifact (e.g., via response time,
items produced, user satisfaction surveys, and
simulation).
Sein et al. A four-stage model of Contains no mention of Argues for the principle of “authentic and
(2011) action design research. validity or knowledge concurrent evaluation” to emphasize a key
claims. characteristic of action design research.
Gregor and A schema for publication Artifact evaluation in terms Distinguishes evaluation inside and outside the
Hevner in design science, of criteria that can include development environment. Utility criteria related
(2013) including evaluation. validity, utility, quality, and to whether performance transfers outside of the
efficacy. development environment.
Prat et al. A taxonomy of evaluation Validity is part of the goal Focuses on “what” (systems of artifacts) and
(2015) methods with five dimension of efficacy and “how” (methods used) in evaluation. Evaluation
dimensions: goal, effectiveness. Validity is involves the “relativeness” of the artifact’s
environment, structure, attained if the artifact works superiority to other solutions. Identifies typical
activity, and evaluation. correctly (achieves goal). evaluation techniques and secondary
evaluations.
Baskerville Genres of inquiry. Provides 18 quality criteria. Provides reflections on genres of inquiry rather
et al. (2015) Framework: design vs. Mentions internal and than evaluation itself.
science and nomothetic external validity.
vs. idiographic.
Venable et Design science Validity is treated as Key purpose of evaluation is to assess how well
al. (2016) evaluations exist along emerging from the strength an artifact achieves the intended utility.
two dimensions: artificial of the evaluation and how
vs. naturalistic and well the artifact
formative vs. summative. accomplishes the purpose.
1270 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
The popular frameworks in Table 2 constitute the established concerned with tests, instruments, or questionnaires
methodological guidance in design science. They provide administered to humans. Over time, quantitative researchers
clarity for understanding the general approach of conducting developed many kinds of validity (e.g., internal, ecological,
research and evaluating artifacts but do not offer guidance on discriminant, external), now widely used in information
validation activities, including how evidence can be provided systems behavioral research (Boudreau et al., 2001). Using
to justify knowledge claims. these validities has been recognized as a “professional
responsibility” (Shultz et al., 1998, p. 266).
Some work in design science has recognized the importance
of establishing validity (vom Brocke, Winter, et al., 2020) Qualitative and interpretivist researchers have argued for
and suggested that existing behavioral validity types (e.g., unique validity concerns in their work, emphasizing the
internal, ecological) might apply to design science importance of the context, setting, and participants, in addition
(Baskerville et al., 2015). In design science, employing to the role of the researchers in creating a natural, trustworthy,
artificial intelligence-based techniques, such as machine confirmable, and dependable account of the research process
learning and natural language processing, it is customary to (Lincoln & Guba, 1985; Onwuegbuzie & Leech, 2007).
report precision, recall, and the F1-score, as well as other Validity in this tradition is a product of social consensus,
confusion matrix metrics (e.g., Abbasi & Chen, 2008; Li et al., where what is valid is based on a “community of
2020). These are not types of validity but are validity-related acceptability” (Moules et al., 2015, p. 172). Reflecting on
because they provide quantifiable measures to establish the these efforts, Creswell and Miller (2000, p. 124) noted “a
validity of claims. They also do not apply to all design science general consensus” that validity is foundational to the
artifacts (e.g., design theories). To establish validity in design acceptance of studies – a view widely shared across
science, we first consider validity in science broadly, which disciplines (Hoyningen-Huene, 2013), including information
we then synthesize with specific concerns of design science.2 systems (Burton-Jones et al., 2021).
In computer science, a discipline closely related to design
science in information systems, researchers in subfields such
Research Validity as machine learning and artificial intelligence have embraced
a common task framework, focusing on shared benchmarks to
The basic idea that knowledge claims should be validated validate new artifacts relative to the state of the art, as reflected
dates to antiquity (Carter, 2019). The scientific term validity in shared leaderboards (Matadamas-Hernández et al., 2012).
This framework has catalyzed major advances in computer
first became popular in the quantitative social sciences (e.g.,
vision and natural language processing. For example, machine
Cronbach & Meehl, 1955) and later became more widely
learning researchers have carefully developed approaches,
used as it was applied to evolving cross-disciplinary beliefs
such as causation analysis and ablation studies, to evaluate
about creating appropriate evaluations (e.g., in which prior
designed artifacts (e.g., Chowdary & Kanhangad, 2022).
knowledge is assessed, and the acceptance criteria are agreed
They employ these approaches under the common task
on) to establish the validity of knowledge claims.
framework to test knowledge claims and contribute to the
shared task knowledge. Nevertheless, despite impressive
To understand validity in design science, we reviewed
progress, the common task framework may have limited the
approximately 7,500 sources from the literature on research
practical applications of resulting models and disadvantaged
validity from information systems (including design science)
evaluation criteria such as “compactness, fairness, and energy
and other research areas, such as computer science, social
efficiency” (Ethayarajh & Jurafsky, 2020, p. 1).
sciences, engineering, medicine, law, and humanities. This
effort yielded 2,418 candidate validities, constituting the largest Each type of inquiry, and sometimes each area (e.g., machine
effort to review validities by more than an order of magnitude. learning), has developed separate validity traditions. Just as
We report on these efforts later when we validate our qualitative and quantitative validity concerns differ, design
framework. Here, we briefly review how validity is used in science validity can be expected to have its own focus. More
science, as this informs our notions of design science validity. than simply borrowing validity types from psychometric,
computer science, or qualitative research, there is an
Initially, validity was narrowly understood as “the closeness of opportunity to address the unique nature of design science,
what we believe we are measuring to what we intended to wherein researchers develop artifacts to bring about desired
measure” (Roberts & Priest, 2006, p. 41). This view focused outcomes and validate knowledge claims about those artifacts.
validity on measurement artifacts, especially in psychometrics, Nevertheless, existing validity research in other disciplines
2 Appendix A evaluates the current state of validation practices.
MIS Quarterly Vol. 49 No. 4 / December 2025 1271
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
has implications for validity in design science, as it deals with Fifth, validity is a matter of degree because the
general validity concepts and ideas. Our review of the validity appropriateness and quality of the reference entity and the
literature led to the following findings that inform design approach taken to validate it may vary. Thus, especially strong
science validity. comparisons are conservative—performed against the best of
knowledge, the state-of-the-art artifact or way of doing
First, researchers agree that systematically evaluated and something, known as the criterion. Both quantitative and
validated scientific research is necessary (Cohen et al., 2013). qualitative researchers (e.g., Moules et al., 2015; Taylor,
Even researchers who conclude that the label “validity” is not 2013) have argued that attaining perfect validity is impossible.
adequate for their research acknowledge the benefits of Each research community determines the norms of what
distilling and sharing successful and proven patterns of constitutes a sufficient outcome of comparison so that the
validation (e.g., Creswell & Miller, 2000; Maxwell, 1992). corresponding knowledge claim can be accepted as
scientifically valid.
Second, sciences seek to advance knowledge claims that
constitute the contributions of the research (Collier-Reed & Finally, to systematize the agreed-upon and widely used
Ingerman, 2013). A study can have many knowledge claims, patterns of reference entities, evaluation procedures, and
with some being the focus of the study (primary claims) and norms for accepting evidence for specific types of knowledge
others taken from prior research (secondary claims). claims, it is necessary to label and organize them into validity
types. Then, claiming a particular validity (e.g., convergent
Frequently, only the former is subject to validation in a study.
validity) can be used as a shortcut for suggesting that the
In the validity context, therefore, a knowledge claim is an
corresponding claim (that two measures are, in fact, related)
assertion about the phenomena of interest that captures the
can be accepted as valid based on the extant scientific norms.
study’s original contribution.
For example, Cook and Campbell (1979) examined threats
and presented approaches to ensure internal validity in social
Third, when validating a knowledge claim, the object of the
sciences, while Lincoln and Guba (1985) proposed steps for
claim is commonly compared to a reference entity—an
demonstrating the trustworthiness and authenticity of claims
abstract or concrete object, the properties or behavior of which
in qualitative studies. These validity templates suggest
can be compared to the proposed idea or object to assess the
specific approaches for identifying the reference entities,
quality of the latter. For example, in computer science,
comparing them, and presenting the findings. This makes it
functional validity is achieved when “the model mimics the
easier to reference and share validation practices, consistently
input-output behaviour of the real system to some acceptable use them, and improve them by identifying connections,
level of accuracy” (Murray-Smith, 2015, p. 30) with the real overlaps, and gaps among validity types, thereby contributing
system being the reference entity. Reference entities appear in to a cumulative tradition.
various forms, including artifacts, existing natural objects
(e.g., a human), and ideas. No matter the research claim, a
reference entity always exists against which to validate the The Design Science Validity Framework
claim. Even for radical innovations or inventions, reference
entities exist against which these can be compared.3
Considering the foundations of validity, we now develop the
design science validity framework.4 We start with the
Fourth, to validate a knowledge claim, researchers engage in
knowledge claims about the focal artifact. Explicating these
one or more evaluation procedures appropriate to that claim.
claims can support scholars in sharing and reusing useful
An evaluation (validation) procedure is a set of tasks
validation procedures.
undertaken to provide evidence of the validity of the
knowledge claim. Commonly, this procedure involves
comparing the focal entity (e.g., the artifact developed in a Design Science Knowledge Claims
design science study) on some dimension(s) to a reference
entity, which may be material or abstract. These procedures The nature of design science claims is rooted in design science
are typically established by consensus within the discipline as utilitarian scientific inquiry (Hevner et al., 2004). A key
(Taylor, 2013). goal of design science is to create artifacts that address real-
3 Consider great inventions of human history, including fire, the wheel, reference artifact can be identified or accessed (e.g., it is proprietary), then
dynamite, the nail, and the printing press. All had manual or less innovative other relevant artifacts or processes can be considered.
artifacts against which they could be evaluated. While the genius of many 4 In the following, we refer to the design science validity framework simply
revolutionary inventions is the extent to which they depart from existing as the “validity framework” unless we intentionally refer to it by its full
artifacts or ways of conducting tasks (the reference entity), when no existing name.
1272 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
world challenges and to generate design knowledge related to Furthermore, the specific causal mechanisms that relate the
these artifacts. For example, Hevner et al. (2004, p. 77) defined design choices (parts of the artifact) to the desired outcomes
design science as research that “creates and evaluates IT can be provided to deepen the design knowledge arising
artifacts intended to solve identified organizational problems.” from the development of the artifact (Gregor & Jones, 2007;
Since then, the understanding of design science has evolved Peffers et al., 2018). Finally, as practitioners are unlikely to
beyond a pure organizational focus, as researchers increasingly implement their solutions in contexts identical to the original
research context presented in an article, it is valuable to
seek to tackle broader societal and individual challenges
specify when and under what conditions and boundaries an
(Weinhardt et al., 2020; Winter et al., 2014). Furthermore,
artifact is expected to attain its outcomes (Hevner et al.,
many artifacts are sociotechnical, coupling software, hardware,
2024). A key task for design scientists is to support other
and processes with individuals, groups, and organizations
researchers and practitioners in reusing artifacts and design
(Thomas et al., 2022). Thus, design science encompasses a
knowledge in new settings (e.g., Iivari et al., 2021).
wide range of social issues and corresponding innovative
artifacts, an inclusive perspective that we adopt. What
The activities of conducting design science produce specific
distinguishes design science from practice is the goal of
types of knowledge claims. A design science knowledge
developing knowledge related to building artifacts (Gregor &
claim is a proposition about an artifact that asserts its
Jones, 2007; Peffers et al., 2018). We therefore define design
contribution to science and society through a particular form
science as research that develops novel artifacts and relevant
or function. For example, Tiefenbeck et al. (2016) developed
design knowledge to address individual, organizational, and
a shower meter and claimed that the particular indication of
societal challenges and opportunities.
water and energy consumed (the form of the artifact)
lowered energy consumption (the artifact’s function)
Many types of artifacts are design science contributions.
compared to showers lacking such indicators.6 Consistent
Common artifacts are models, methods, instantiations, and
with the aims of design science, design science knowledge
design theories and theory components (e.g., constructs, design
claims propose that an artifact built through a specified
principles) (Gregor & Hevner, 2013). Artifacts are complex
approach leads to a desired outcome, that the outcome is
entities with multiple interrelated parts or components.5 They
caused by the specific design properties of the artifact, or that
are also commonly taken to be subsystems of larger systems,
the outcome is expected to hold in a specific context or
such as organizations or broader technical systems. Considering
across different contexts. We label these types of knowledge
this diversity, we define a design science artifact as an abstract
claims criterion, causal, and context, respectively, and
or concrete entity created as a focal contribution of a design
elaborate on them below.
science project to attain desired outcomes at the individual,
organizational, or societal level.
Criterion claims: In every design science paper we
reviewed, the authors make one or more claims about the
The basic tenets that design science provides solutions to
expected outcomes of the artifact, such as its benefits or
problems and generates prescriptive design knowledge are
utility for addressing a challenge or opportunity. We define
central to design science knowledge claims. Specifically, to
a criterion claim as a knowledge claim about the utility of an
assess the contribution of a given artifact, the artifact must be
artifact. There is always an existing or alternative way of
superior in some way (e.g., faster, more efficient, cheaper) to doing something, so criterion claims implicitly or explicitly
existing solutions (Padmanabhan et al., 2022) and the present a comparison to such existing entities or processes
approach used to create the artifact must be specified (Hevner (also known as the state of the art or criteria) (Padmanabhan
et al., 2004). To function as a science and allow others to et al., 2022). For example, authors may claim to have
benefit from the accrued design knowledge, researchers need to developed a more effective construct search engine (Li et al.,
communicate knowledge about how the artifact was built—for 2020) or a novel design theory of tailorable technology
example, through sharing code in a repository or describing (Germonprez et al., 2007). Such claims state or assume that,
how the artifact functions at a conceptual level (Burton-Jones respectively, conventional search engines could work better
et al., 2021; Hevner et al., 2024). by extracting theoretical constructs from papers or that
typical design theories do not address tailorable
5 Each artifact type also has many subtypes. For example, the subtypes of an instantiation, by constructing a system or implementing a method, or
model include frameworks, taxonomies, ontologies, simulations, and possibly in rare cases through deductive logic.” The design knowledge
mathematical models. claim is a broader concept: As we show in the paper, knowledge claims
6 In the context of design theories, Gregor and Jones (2007, p. 327) apply to any artifact, and to be validated, they do not require instantiating
advanced a related notion of “testable propositions or hypotheses,” their components, even in the case of design theory.
explaining that these propositions about design theories are tested “through
MIS Quarterly Vol. 49 No. 4 / December 2025 1273
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
technologies. We refer to these claims as criterion claims It is not always possible to know how or why something
even though a claim itself does not need to explicitly specify works, especially when dealing with complex technologies,
the criterion. innovative artifacts, and “inventions” (Gregor & Hevner,
2013). Hence, not all papers make such claims; in our survey
Criterion claims are especially strong when the comparison of design science papers, 50% made causal claims.
artifact is the commonly agreed-upon state of the art
(Padmanabhan et al., 2022). For example, Larsen and Bong Context claims: Artifacts are always created in some context
(2016) compared the performance of their search algorithm to to address a given challenge or opportunity. However, the role
an EBSCO Host search engine criterion, whereas Li et al. of context is not always considered in design science. To
(2020) made an arguably stronger claim by comparing their support practitioners in implementing artifacts, context claims
search algorithm to both EBSCO Host and Google Scholar— explicate the situations or conditions in which the proposed
generally acknowledged as the state of the art for academic outcomes of the artifact are expected to hold. Accordingly,
search. In our examination of design science articles (reported criterion and causal claims are generally considered more
later), we found that all papers had criterion claims that rigorous when evaluated in multiple contexts or contexts that
implicitly or explicitly indicated outcomes that were better are more like the intended use context of the artifact.
than existing artifacts or processes.
Not all design science papers make context claims. One
Causal claims: In the long term, a criterion claim is exception is action design research, where the setting in which
insufficient to ensure scientific progress. After criterion the artifact is implemented, a real organization (Sein et al.,
claims have been established, researchers may (within a 2011), is the context in which any claims about the artifact are
study that establishes a criterion claim or in subsequent intended to apply. A context claim can be broadened (and
studies) wish to deepen the design knowledge by hence, the scope of the criterion or causal claims strengthened)
substantiating claims about which design features of the with suggestions that the artifact works beyond its original
artifact produce their claimed outcomes. We label such setting, such as in similar or even distinct settings. Further, a
claims causal claims, given the fundamental interest of context claim can help delineate the generalization of findings.
science in causes and effects (Salmon, 1998). A causal claim For example, Lukyanenko et al. (2019) explicitly claimed that
is a knowledge claim about the extent to which specific parts
their instance-based method of data collection is especially
of an artifact cause a specific utility.
effective for open-ended tasks in large-scale citizen science
projects, but also claimed that it is not expected to yield benefits
While providing code or descriptions of an artifact helps
for closed-ended collection in microtask crowdsourcing.
support the value of an artifact and makes it more accessible
to replication and extension, advancing causal claims can
In our sample of design science papers, 14% of papers made
help build better artifacts and develop new theories of context claims. This number may have been depressed by
technology. For example, Abbasi and Chen (2008) advanced authors who did not explicitly make such claims, even when it
several causal claims when stating that CyberGate’s feature was likely that such claims could have been supported with the
sets were better at representing information types than evidence provided. If so, this represents an opportunity for
baseline feature sets commonly used in prior systems (note researchers to consider advancing context claims (so that others
the presence of a criterion claim as well). They conducted reading their work can better appreciate the other contexts in
separate evaluations for each of the extended feature sets, which the solutions they developed might also be useful).
namely topic, opinion, style, genre, and interaction
information, to establish the causal influence of each on the Figure 1 summarizes the validation process based on the
artifact performance (the criterion coming from the importance and prevalence of knowledge claims. The figure
performance of an artifact employing all the features). implies that each paper makes at least one criterion claim. This
may be sufficient for novel artifacts. As Gregor and Hevner
Causal claims are not restricted to machine learning or even (2013, p. 346) suggest, novel artifacts are “interesting
instantiated artifacts. In our evaluation, we evaluate causal applications where little current understanding of the problem
claims about the value of parts of our own design science context exists and where no effective artifacts are available as
validity framework. In fact, given that most types of design solutions.” Then, depending on the artifact’s novelty, a paper
science artifacts are not instantiated, qualitative methods play may additionally advance causal and/or context claims to
a major role in evaluating these artifacts. These methods, in improve the understanding of why and where the artifact
turn, can be grounded in justificatory knowledge (e.g., kernel works. Causal claims require the simultaneous or previous
theory) that suggests the causal mechanisms connecting
establishment of a criterion claim; context claims require the
artifact features to target outcomes (Gregor & Jones, 2007).
establishment of either a criterion claim or a causal claim.
1274 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Figure 1. Claims and Validation Process
The three types of knowledge claims can be made with respect which is a system of concepts and propositions (Gregor &
to all types of artifacts. As discussed, abstract artifacts (e.g., Jones, 2007), is an abstract artifact.
design theory, conceptual models) can be instantiated and (via
instantiation) can be shown to have measurable impact on the Abstract artifacts can be used in developing material artifacts
world. Furthermore, qualitative techniques, such as such as shower meters. Often, there are two separate but
counterfactual analysis and stakeholder interviews, can be related artifacts—the theory (e.g., design propositions) and
used to evaluate criterion, causal, and context claims for the material artifact generated from it (e.g., the shower meter).
abstract entities. The types of claims are driven by the desired Artifacts are components of larger systems, such as
knowledge contribution, not the artifact type. sociotechnical systems of people and artifacts (Chatterjee et
al., 2021; Winter et al., 2014). For many projects, it is
important to consider the broader systems in which artifacts
Design Science Artifact and Comparison Entities are embedded because the knowledge claims may be made
with respect to systems-level impacts. If a researcher seeks to
We define design science validity as the extent to which design the sociotechnical system itself as an artifact (see
knowledge claims about a focal artifact are supported by Thomas et al., 2022), criterion, causal, and context claims can
evidence. In line with the three types of knowledge claims, be made about this sociotechnical system.7 At the same time,
three general types of design science validity exist: criterion, if the focus is on the properties and behavior of the artifact
causal, and context. By supporting their respective claims, (e.g., smart shower meter) embedded in a sociotechnical
these validity types advance the practice of design science in system (e.g., smart city), the system provides an
three important ways. First, criterion validity is used to implementation setting for the artifact, enabling context
support claims about the outcomes of designing and using the claims about the artifact to be made. Note that the focal artifact
artifact, aimed at bringing about the desired change. Second, and the comparison reference entity exist within (typically
causal validity is used to support claims about the contribution different) sociotechnical systems, creating context validity
of a specific design (artifact feature, part) to the utility of an challenges.
artifact. Third, context validity addresses the extent to which
knowledge claims hold for the intended context or additional To derive the categories of reference entities, we considered
contexts. Within these broad categories, we propose more the major types of artifacts produced by design science—
specific validity types based, primarily, on the type of constructs, models, methods, instantiations, and design
reference entity and, secondarily, on the nature of comparison theories, along with existing natural objects that can be used
between the focal artifact and the reference entity. as criteria (vom Brocke et al., 2020b; Gregor & Hevner, 2013;
Hevner et al. 2004; March & Smith, 1995). Table 3 outlines
The focus of design science validity is on claims about a focal the list of reference entities to which a focal artifact can be
artifact. Some artifacts are material and others are abstract compared. Having the reference entities allows us to explicate
(Gregor & Hevner, 2013, p. 341). For example, Tiefenbeck validity types and formalize the specific validation procedure
et al.’s (2016) shower meter is material, whereas a theory, that researchers can use to support their knowledge claims.
7 Once a customer relationship management (CRM) system (the focal Furthermore, by considering the organizations with CRM relative to those
artifact) is placed in the broader social and physical system of an without CRM or the same organization before and after the introduction of
organization, we can evaluate attributes of the larger system, including the the CRM, we can validate claims about the impact of the CRM or its
organization (e.g., customer satisfaction, fairness, sales, profit). components on outcomes of interest.
MIS Quarterly Vol. 49 No. 4 / December 2025 1275
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Table 3. Categories of Reference Entities
Category Subcategory Details
Instantiated Criterion instance Category includes criterion artifacts (e.g., the search engine
entities A real-world entity that becomes a Google Scholar), real-world objects (e.g., a human chess
Output-generating standard against which a focal master), real-world processes (e.g., hiring employees), and
entities. When in artifact can be compared. sensors reporting on real-world states (e.g., temperature or
use, they create rainfall).
change in the world, The responsibility of the researcher is to justify that the
which can be criterion instance serves as a reasonable standard for
measured and comparison.
recorded. Outputs
of the reference Instantiations operationalize constructs, models, methods,
entity may be in the and design theories into material solutions (e.g., apps,
past, present, or platforms, enterprise systems).
future. Other
Criterion instances are used to demonstrate the superior
aspects than the
performance of the focal artifact or the ability of the focal
outputs can also be
artifact to approximate the output, structure, or features of the
compared.
criterion entity.
Manipulated artifact Constructed by removing or replacing a part of the focal
An artifact derived from the focal artifact.
artifact; typically developed within
the same study and manipulated to
enable inferences from comparing
two artifacts.
Uninstantiated Theory (and its components: Design theories and their components (e.g., constructs,
entities constructs and design principles) design principles) and non-design theories (e.g., theories of
Objects of A system of concepts intended to explanation and prediction), which can provide design-
comparison that are explain, predict, or guide action. relevant knowledge for focal artifacts.
blueprints for
Model A model represents some aspect of reality; commonly
concrete material
artifacts. A conceptual representation of ignores aspects not relevant to modeler; may introduce
some aspect of reality created to purposeful biases.
Unless instantiated,
these entities do not increase understanding or facilitate A model represents a domain where design interventions
produce material action. occur, or there are other design artifacts and is assessed with
outputs. They respect to utility or correspondence to truth.
commonly require
Method Methods can be found in a variety of different areas. For
interpretation by an
agent such as a A self-contained, logical sequence example, requirements analysis, process control, and
human expert. of steps used to accomplish a task. checklists.
Validity Types criterion validity has two subtypes: criterion efficacy validity
and criterion characteristic validity.
Criterion validity types: As indicated in Figure 1, all design
science projects should make a criterion claim to show that the Criterion efficacy validity supports claims about the
designed artifact provides some benefit. Doing so requires instantiated artifacts (Table 3) when the focal artifact and
engaging a criterion validity type. Criterion claims (and causal reference entity have comparable outputs. Criterion efficacy
claims, as we show later) can be compared in two ways: validity thus deals with criterion claims that are supported by
through their efficacy or through their characteristics. Efficacy comparing the efficacy of the focal artifact to that of an
comparisons consider the similarity of the artifact’s outputs to instantiated entity argued to represent a standard. These types
other output-generating entities, whereas characteristic of validity support claims that the outputs of the artifact (or the
comparisons assess the similarities among the characteristics effects of such outputs on a sociotechnical system) have utility
of the artifact and its reference entities (Table 3). Therefore, relative to the outputs or effects of a reference entity.
1276 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Two subtypes of criterion efficacy validity can be distinguished, Criterion model validity (model validity) is the extent to which
depending on whether time is important. If so, predictive a focal artifact is consistent with a model. Although this validity
validity, with proper registration of the predictions before the type did not occur in the sample of design science papers we
results are generated by the reference entity, yields the strongest reviewed, the consideration of criterion model validity was
validity for claims. However, in design science, predictive present in our literature review. For example, Refsgaard et al.
validity is more often evaluated against future data that exist at (2006, p. 1596) suggested that when developing the code for a
the time of artifact creation but are not made available to the simulation model (focal artifact), it is essential to establish that
artifact until after the validation. If time is not a factor in the the “model code is in some sense a true representation of a
predictions, future data is not available, or a weaker validation conceptual model” (e.g., a model developed by experts) of the
is sufficient, concurrent validity can be evaluated. When a real-world system (e.g., of an ecosystem).
predictive claim is not made, concurrent validity can be
employed to examine the outputs of the focal artifact relative to Finally, criterion method validity (method validity) compares a
reference outputs. Often, available cases are split through cross-
method to an existing method as a self-contained, logical
validation into “train,” “validation,” and “test” sets, wherein the
sequence of steps used to accomplish a task. Criterion methods
focal artifact’s performance relative to true values in the
enable the evaluation of a focal artifact or part of a focal artifact
“validation” and “test” sets are types of concurrent validity. In
against other entities (natural entities or artifacts and their parts).
casual contexts, the term “criterion efficacy validity” can be
Piramuthu and Doss (2017) provided an example when they
assumed to refer to concurrent validity.
evaluated their artifact—a protocol for the simultaneous
authentication of multiple radio-frequency identification tags.
Criterion characteristic validity deals with criterion claims that
They used formal proof to validate that the protocol met the
compare characteristics of the focal artifact to those of a
strongest security requirement (Avoine et al., 2009).
reference entity argued to represent a standard. For
characteristic validities, an agent (most often a human) is
Causal validity types: Like criterion validity, causal validity
commonly involved in the evaluation because: the reference
has two subtypes: causal efficacy validity and causal
artifact does not produce outputs (as is the case for theories,
characteristic validity. Causal efficacy validity deals with
models, and methods); the output is not directly comparable to
causal claims supported through evaluation relative to the
the reference entity (as can be the case when comparing the
efficacy of a manipulated version of the artifact that has
outputs of two generative AIs); the artifact is instantiated but a
intentionally different parts (compared to the focal artifact).
characteristic of the artifact (such as its interface) contains the
The manipulated artifact is typically developed in the context
contribution; or the artifact is compared to the respondent’s
of the same study by the same research team and is
experiences with relevant artifacts or processes (such as with
manipulated to permit inferences arising from comparisons of
the evaluation of perceived usefulness). All such cases are ones
the two artifacts. This is sometimes referred to as an ablation
in which a criterion characteristic validity is employed.
study, as introduced by Newell (1975), and commonly found
in machine learning (e.g., Abbasi et al., 2012; Abbasi &
Characteristic validities allow for the evaluation of aspects of
Chen, 2008; Etudo et al., 2017).
the artifact that efficacy evaluations are unable to evaluate.
They are more flexible and enable comparison of the non-
Causal characteristic validity addresses causal claims that are
identical outputs or outputs that cannot be automatically
supported by comparison to the characteristics of a
compared (e.g., perceptions of usefulness of a medical ontology
manipulated artifact that has intentionally different
or a website). Whether evaluation is based on the direct
comparison of outputs or an artifact’s characteristics, specific components. One way to achieve this difference is by
validity types are based on the comparison entity (Table 3). For removing or changing a component (a part). As with causal
example, criterion instance validity (instance validity, for short) efficacy validity, the comparison entity is typically developed
is the extent to which claims about an artifact relative to an in the context of the same study by the same research team and
instantiated reference entity are supported. Abbasi et al. (2018) is deliberately manipulated to enable inferences from
engaged with criterion instance validity to validate a utility comparing the two artifacts. For example, Umapathy et al.
claim. The authors asked the organization to estimate the (2008) developed two versions of their focal artifact: one
savings realized by implementing the system versus continuing permitting the selection of integration patterns with the
with the current business process. support of speech acts (focal artifact) and one with no support
(reference artifact). The researchers performed an experiment
Similarly, theory validity addresses the extent to which claims in which participants were given a business process design
about a focal artifact relative to a theory artifact are supported. task (with a list of specific task elements) to produce a
For example, Lukyanenko et al. (2019) developed a citizen modified business process model and notation (BPMN)
science platform with design features that they claimed model of an enterprise integration. The models were evaluated
corresponded to relevant principles from a design theory. by experts and the perceived number of errors was compared.
MIS Quarterly Vol. 49 No. 4 / December 2025 1277
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Another approach relies on counterfactual reasoning (Collins artifact is being used. For example, Zaitsev and Mankinen
et al., 2004). Comparing the focal artifact to a version that has (2022) worked with participants in Cambodia to develop an
a component removed can validate that the component does app that was used in a real-world setting.
not have a causal impact on the performance of the artifact and
can be removed for parsimony. External validity is defined as the extent to which criterion or
causal knowledge claims are supported through an evaluation
Context validity types: The context validity type supports in more than one sociotechnical system. When the
claims about the setting and conditions (e.g., laboratory vs. sociotechnical systems in which the focal artifacts are
real-world sociotechnical system, used by target users or their evaluated differ and the focal artifact retains its utility, higher
surrogates) in which the artifact is evaluated. The goal here is external validity is realized. For example, Zaitsev and
to assess the extent to which the criterion and causal claims Mankinen (2022) used an action design research approach to
related to the artifact are supported in a setting that is in some develop an app to improve financial literacy through training.
way like the target sociotechnical setting or generalizes across The original development occurred in Cambodia, but the
different settings. Hence, context validity evaluation artifact was later adapted and used in Nepal, providing
procedures deal with the differences in conditions and external validity, with the authors concluding that “the
settings. The context claims can either be made against the original design, already flexible and minimalist, created
context of artifact evaluation relative to the target according to the design principles, provided a good foundation
sociotechnical system or another context. This results in two for localization” (p. 106).
subtypes of context validity: ecological (focusing on the
attributes of the original evaluation context relative to those of
the target sociotechnical system) and external (focusing on The Design Science Validity Framework and
evaluation in additional sociotechnical systems). Its Application
A claim’s ecological validity increases with the similarity
Figure 2 shows our design science validity framework. The
between the evaluation sociotechnical system and the
framework establishes the relationship between the three
sociotechnical system for which the artifact is intended. Some
types of claims about the focal artifact and the specific validity
design science approaches, such as action design research,
types used to provide evidence in support of these claim types,
tend to have high ecological validity because evaluations are
via specific types of comparison. Table 4 formally defines
performed in naturalistic organizational settings in which the
each of the validity types.
Figure 2. Design Science Validity Framework
1278 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Table 4. Design Science Validity Definitions
Design science validity The extent to which knowledge claims about a focal artifact are supported by evidence.
Criterion validity The extent to which knowledge claims about a focal artifact are supported through evaluation
compared to a reference entity argued to represent a standard.
Criterion efficacy The extent to which knowledge claims about the efficacy of a focal artifact are supported
validity through evaluation compared to the efficacy of a material reference entity argued to represent
a standard.
Predictive validity The extent to which knowledge claims about the efficacy of a focal artifact are supported
through evaluation of its accuracy compared to a reference efficacy that came into existence
after the data used to create the artifact.
Concurrent validity The extent to which knowledge claims about the efficacy of a focal artifact are supported
through evaluation of its efficacy compared to a reference output that came into existence in
the same period as the data used to create the artifact.
Criterion characteristic The extent to which knowledge claims about the characteristics of a focal artifact are
validity supported through evaluation of its characteristics compared to the abstract characteristics of
a reference entity argued to represent a standard.
Instance validity The extent to which knowledge claims about the characteristics of a focal artifact are
supported through evaluation of its characteristics compared to the abstract characteristics of
an instantiated reference entity argued to represent a standard.
Theory validity The extent to which knowledge claims about the characteristics of a focal artifact are
supported through evaluation of its characteristics compared to the characteristics of a theory
reference entity argued to represent a standard.
Model validity The extent to which knowledge claims about the characteristics of a focal artifact are
supported through evaluation of its characteristics compared to the characteristics of a model
reference entity argued to represent a standard.
Method validity The extent to which knowledge claims about the characteristics of a focal artifact are
supported through evaluation of its characteristics compared to the characteristics of a
method reference entity argued to represent a standard.
Causal validity The extent to which knowledge claims about the impact of a part of a focal artifact are
supported through evaluation compared to a manipulated artifact missing that part.
Causal efficacy The extent to which knowledge claims about the impact of a part of a focal artifact on that
validity artifact’s efficacy are supported through an evaluation of its efficacy compared to the efficacy
of a manipulated artifact missing that part.
Causal characteristic The extent to which knowledge claims about the characteristics of a part of a focal artifact are
validity supported through an evaluation of its characteristics compared to the characteristics of a
manipulated artifact missing that part.
Context validity The extent to which criterion or causal knowledge claims are supported through an evaluation
in a specific context.
External validity The extent to which criterion or causal knowledge claims are supported through an evaluation
in more than one sociotechnical system.
Ecological validity The extent to which criterion or causal knowledge claims are supported through an evaluation
in a sociotechnical system corresponding to real-world sociotechnical systems for which an
artifact is intended.
MIS Quarterly Vol. 49 No. 4 / December 2025 1279
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
In general, different validity types are appropriate, depending Evaluation and Application of the
on the kinds of claims researchers wish to make. As our
Framework
framework shows, there are three main types of claims,
corresponding to the three main types of validities. Hence, our
To assess the framework and simultaneously demonstrate
framework allows researchers to determine appropriate validity
types based on the nature of the knowledge claims about an how to use it, we applied the framework recursively to itself.
artifact. Once researchers have decided on a type of claim, they A framework (a type of model) should have utility, which
should follow that claim type from the top until they find an means, for example, that it must be seen as useful by its
appropriate bottom-level validity type to support that claim. potential users (Hevner et al., 2004; March & Smith, 1995).
A framework should also be parsimonious while faithfully
For example, Koornneef et al. (2020) proposed a method to capturing the key domain’s concepts (National Academies,
improve the process of identifying relevant information and 2022).
options for resolving aircraft troubleshooting/maintenance
issues between flights. The authors claimed that their prototype We formulate several knowledge claims about the validity
supported the faster retrieval of information relevant to issue
framework, which we then validate. We advance several
resolution (a criterion claim, see Figure 2). They compared their
criterion claims, followed by context and causal claims to
prototype to the current practice in the industry of searching for
illustrate the usage of all types of claims and different types
relevant information in maintenance manuals. As the prototype
of validity. First, we claim framework utility as perceived by
and manual search methods provided comparable output (i.e.,
its potential users—design scientists. These are criterion and
relevant issue information), this is an example of criterion
context claims supported by evidence of model validity and
efficacy validity with a specific type of concurrent validity (as
time of comparison is assumed to play no role). To further ecological validity. Second, we claim framework utility in
bolster their claim, the authors performed an experiment in systematizing existing validation procedures (named and
which advanced maintenance trainees were asked to locate unnamed), as supported by evidence of model validity.
relevant information using either the prototype or the manual Third, we claim framework utility in systematically
method. The authors measured the search time in both cases and capturing and organizing existing design science validity
found that the prototype provided faster search times. If an types as proposed and defined across disciplines. These are
evaluation supports the claim, only one leaf-node validity type criterion and context claims supported by evidence of model
may be necessary. Should the authors determine that their validity and external validity. Finally, we claim that the
artifact is not novel enough to warrant publication in their target
framework’s components are sufficient for attaining utility,
outlet, they can deepen the contribution by making a causal
as supported by evidence of causal characteristic validity.
claim. While Koornneef et al. (2020) already had an efficacy
validity evaluation, in a hypothetical scenario, they may then
have added a causal efficacy validity by evaluating which parts
Claim 1: The Criterion Claim and Context
of their artifact contributed most to the speed of retrieving
Claims With Target Users
relevant information.
For Claim 1, we evaluated criterion and context claims by
This example illustrates how the framework represents
existing design science practices and how it can be used undertaking two applicability checks (Rosemann & Vessey,
retrospectively to analyze an existing validation and better 2008), a common type of design science evaluation (e.g., Li
understand why certain choices were made. It can also suggest et al., 2020; Lukyanenko et al., 2019). The applicability
alternatives (e.g., evaluating prototypes by asking for human check is a composite evaluation touching on several validity
judgment, resulting in characteristic validity types), thus types. However, for evaluating the validity framework the
showing the possibility of using the framework to guide the applicability check is effective for addressing model validity,
design science validation process. wherein participants compare our framework to their model of
an ideal framework and other relevant frameworks. Because
We further demonstrate the scope of the framework by
it engages the likely users of the framework and asks them to
considering sample work from the design science literature.
employ it in the context of their work, the applicability check
We scope this demonstration by considering the artifact types
also provides evidence of ecological validity. Our evaluation
proposed by March and Smith (1995) and Gregor and Hevner
took place in the context of design scientists who had
(2013): instantiations, design theory, methods, and models.
extensive experience with evaluation and exposure to existing
For each of these artifact types, Table 5 presents a sample
evaluation frameworks.
paper and identifies the artifact, claims, and validity presented
by the authors.
1280 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Table 5. Exemplar Validations
Artifact and artifact type Knowledge claim Validity type Evaluation
Meth et al. (2015) propose a requirements Use of the tool allows users to Concurrent Experiment to evaluate
mining tool, an instantiation. identify requirements with validity whether users accurately
greater accuracy than without identify all requirements
the tool. using the tool.
Ramakrishnan et al. (2023) propose design Principles have accessibility, Theory validity Focus group evaluation of
principles for platform-enabled knowledge importance, novelty and design principles.
commons, a theory. insightfulness, actability and
guidance, and effectiveness.
Sedrakyan et al. (2017) propose a feedback- FIRP simulation improves the Model validity* Factorial experimental
inclusive rapid prototyping (FIRP), a method. understanding of the behavioral design evaluating
aspects of a model. understandability of
method.
Valecha et al. (2013) propose a shared Model is complete and correct Model validity Focus groups with
vocabulary for message standardization in the for covering the communication emergency responder
emergency response domain, a model. needs of emergency experts.
responders.
Note: *The reference entity may be different from the artifact type, as it deals with establishing the baseline. For example, participants may draw
on their model of the world to assess some aspects of the proposed method.
Prior evaluation frameworks, including those of Prat et al. for evaluations; organizes existing validities into these meta-
(2015) and Venable et al. (2016), focus on patterns of categories; and identifies the specific comparisons and
evaluation and on contemporaneous and post hoc strategies the claim—evaluation—evidence argumentation structure of
for evaluation, respectively. By coding six dimensions of the evaluations themselves.
evaluation techniques and criteria, Prat et al. identify specific
techniques (e.g., observation, description, experiment, In the first applicability check, the validity framework was
dynamic analysis) and specific research approaches (e.g., presented at a regional information systems workshop
qualitative, experiment, simulation, metrics) that are used in attended by both behavioral researchers and design scientists;
evaluation. Venable et al.’s (2016) framework focuses on the our focus was on the initial assessment of utility and making
artificial/naturalistic context in which evaluation takes place any adjustments before we engaged the final cohort of design
and how those evaluations can be formative (taking place science experts. Fifteen participants were trained in using the
during the project) or summative (taking place at the validity framework and tasked with organizing four validity
conclusion of the project). definitions and four design science evaluations into the
framework and responding to an open-ended survey. The
In contrast, our validity framework provides the underlying results suggested that the framework would be useful to
scientific reasoning for validating knowledge claims through design scientists and other researchers. For example, the
the evaluation process. By this, we mean the degree to which framework was described as “a thought-provoking and
evidence gained through an evaluation process supports the refreshing perspective.” Other comments noted that the
knowledge claims made by researchers about the focal framework was quite complex, especially for researchers with
artifact. Furthermore, our analysis shows that evaluations in limited design science experience. In response, we added a
design science are always comparisons: performance criteria process for selecting which validity types to use in a research
compared with existing criterion artifacts (or existing ways of project and streamlined the framework.
accomplishing the same outcome), desired artifact
characteristics compared with existing artifacts, or After incorporating the feedback into the framework (the final
comparisons within and/or between contexts of artifact version of which is shown in Figure 2), we performed the
application. In articulating the relationships among criterion, second applicability check among leading design scientists to
causal, and context validities, our validity framework goes evaluate the framework’s importance (criterion claim),
beyond prior evaluation frameworks. We show the processes accessibility (context claim), and suitability (context claim).
by which evaluations are performed and demonstrate how the
validity of types of knowledge claims is established. By The 11 participants were design scientists with varying levels
making these relational comparisons explicit, our framework: of post-Ph.D. academic experience (an average of 13 years).
provides meta-categories (e.g., criterion, causal, and context) For those with Google Scholar accounts (nine participants),
MIS Quarterly Vol. 49 No. 4 / December 2025 1281
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
their average citation count was 4,981. An examination of Rosemann and Vessey (2008) define importance as research
their papers found that 36% had cited Prat et al. (2015) or “that meets the needs of practice by addressing a real-world
Venable et al. (2016). The applicability check was conducted problem … in such a way that it can act as the starting point
online to include scholars from various locations, research for providing a solution” (p. 3). We consider the process of
areas, and subcommunities of design science. These evaluating this aspect to be an instance of criterion validity. In
participants employed a variety of methods, considering our context, design scientists are practitioners in the real world
diverse research topics and types of analysis. Their research
who themselves need to validate knowledge claims about
covered a broad set of topics, including data and knowledge
artifacts. Accessibility is a criterion validity that
modeling, analytic and machine learning modeling, data
“encompasses whether the research is understandable,
science, business process change, simulation, and design
readable and focuses on results rather than the research
theory. We specifically invited participants across a broad
process” (p. 3). Finally, suitability is defined as the extent to
spectrum to include participants across design science as a
which the research can “[meet] the needs of practice” (p. 3),
whole. Participants were regular contributors to WITS,
which we take to mean the extent to which researchers view
DESRIST, and other design science conferences. The stages
the framework as appropriate for the target context. These
of the applicability check are described below.
three evaluations all address model validities as well as
context validity, given their evaluation in a setting similar to
Preparation: Participants were asked to describe examples of
the real world.
the validation processes they used in ongoing research or a
recently completed project. These existing processes, part of
the mental models of the experts, were the benchmarks against Participants agreed that the framework is important for
which participants assessed our framework. clarifying and providing structure to the increasingly complex
requirements for validation methods, criteria, and strategies.
Overall, participants exhibited a consistent understanding of This importance was evidenced by comments such as “it
the need for artifact evaluation and validation, but supports a systematic approach to validation” and “a
demonstrated a limited understanding of the types of validity framework like this can give researchers an accepted standard
that aligned with their evaluations and lacked a vocabulary to to point to as they try to validate their own design science
describe their validations. In multiple cases, validity types artifacts.” Other comments acknowledged that the framework
were discussed in psychometric terms (e.g., construct validity) reduces complexity, connects knowledge claims to validation
or terms related to utility and efficacy (e.g., proof of concept, strategies, and provides details useful for elaborating validity
proof of value). Most participants focused on the processes by claims. All these comments support our criterion claim.
which evaluations were performed (e.g., field experiments,
lab experiments), rather than the role of validations in Despite only having a brief introduction to the framework,
supporting claims about their artifact.
accessibility was evidenced by comments such as: “It is a
good thing I have learned about your validity framework early
Introduction to the design science validity framework:
in my project.” One participant found the framework to be
Participants then attended an hour-long online session during
immediately accessible, stating: “I can use the framework ….
which the author team presented the validity framework.8
the framework provided a validation that my evaluation is
Following the explanation of the framework and the extended
good enough, but I should have elaborated a few more details
example, participants were asked to use our process to
in my evaluation for reviewers.”
determine validity types in their projects.
The final applicability precursor, suitability, was also reflected
Feedback: When finished the task, the participants filled out
in comments: “As a DSR scholar and author, the framework
a survey containing six open-ended questions and a set of
helps me to plan the validation of my work early on. … As a
questions about artifact usefulness and their intention to use,
reviewer and editor, I will be able to point to a shared
applying Likert-type scales from Venkatesh et al. (2003). The
understanding of validity in DSR. When assessing the value
responses, both qualitative and quantitative, indicated that
of a DSR paper, I can use the framework to identify strengths
participants considered the validity framework to be
and potentials for improvement. Or to prompt the authors to
important, accessible, and suitable (Rosemann & Vessey,
share the aspects of their DSR work which they have excluded
2008) for meeting the identified needs of the community and
from the paper but are relevant to establish its validity.”
believed it would be useful for their own research.
8 The presentation is available in the transparency materials at
https://osf.io/ca6vg/.
1282 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Two concerns were raised regarding the future implications of 121 design science papers identified by Prat et al. (2015) from
the framework. The first was that the framework could be used the Association for Information Systems (AIS) Senior
to inhibit the publication of design science because “reviewers Scholars’ Basket of Eight journals (April 2004 to December
may disagree on which validity types are required.” 2013). Second, we analyzed 1,233 additional candidate papers
Participants agreed that this is not a flaw in the framework from the AIS Basket of Eight from 2014 to 2017. We then
itself. It is inappropriate to use the framework as an argument manually coded these 1,233 papers based on the inclusion
for additional evaluations. As noted above, additional schema of Prat et al. (2015). Eighty-six papers were coded by
evaluations are justified only when either the evaluations the third author as design science and cross-checked by the
performed are not aligned with the knowledge claims made or second author. There was 100% agreement that all were
the contributions of the paper with the existing knowledge design science papers. The original 121 papers from Prat et al.
claims are deemed by the review team to be insufficient. In (2015), plus our 86 papers, yielded a total of 207 papers
the latter case, any additional evaluations reviewers propose published between April 2004 and December 2017.
should be appropriate to additional knowledge claims.
To capture articles that followed the design science approach
The second concern was the potential for increased costs and but did not explicitly use the phrase “design science,” we
time requirements for producing and reviewing design science created feature sets based on a list of design science keywords
work because of increasing demands for validity procedures. as well as citations of top design science papers. We then
We updated our initial framework to better explain the trained a machine learning model for distinguishing relevant
knowledge claims and the process of applying the framework manuscripts in the full set of manuscripts, based on the process
to protect against such use of the framework. described by Larsen et al. (2019). We applied a combination
of machine learning and manual evaluation to expand the
Participants responded on a 7-point Likert scale to questions years of coverage from 1994 to 2019 and the sources to
about the usefulness of the framework (μ = 5.64; σ = 1.04), a include the AIS Basket of Eight, as well as Decision Support
common applicability check question in design science (e.g., Systems, ACM Transactions on Information Systems, and the
Li et al., 2020; Lukyanenko et al., 2019). They were also proceedings of the International Conference on Design
surveyed about their intention to use the framework (μ = 6.15; Science Research in Information Systems and Technology
σ = 0.92) relative to their existing process, another criterion (DESRIST) and the International Conference on Information
claim that, when evaluated in the target setting, doubles as a Systems (ICIS). After downsampling the last four sources, we
context claim. For usefulness, one outlier indicator reflected ended up with 527 design science papers.
the second concern about whether the framework would (at
least initially) slow down research tasks. Without this From our corpus, we randomly sampled 32 empirical articles,
indicator, usefulness increased markedly (from μ = 5.64 to μ which the fourth and sixth authors independently coded,
= 6.14; σ = 1.03). identifying 79 evaluation descriptions. The first and third
authors then independently coded each evaluation description
The one participant who worried that the framework might be using the framework. The coders agreed in 76.3% of cases,
difficult to use also intended to use it, stating that “the resulting in a Cohen’s kappa of 0.703. Disagreements
existence of a framework like this can give researchers an generally concerned what the original authors intended to
accepted standard to point to as they try to validate their own claim rather than how to interpret the validity framework.
design science artifact [claims].” All participants indicated From this exercise, we concluded that evaluations found in the
that they intended to use the framework once it became papers reviewed could be classified using the validity types in
available. We therefore concluded that the applicability our framework, demonstrating model validity. However, two
checks established model validity and added initial evidence validity types, theory validity and model validity, were not
of ecological validity. used in the papers we sampled (Table 6).
Claim 2: The Criterion Claim of Framework Claim 3: The Criterion and Context Claims of
Completeness Representational Power
We validated the claim that the validity framework is The formalization of shared disciplinary conceptualizations
complete in representing existing evaluations in published accelerates scientific progress (National Academies, 2022).
design science articles. Since the framework is a model, it Other disciplines also develop and validate artifacts, and the
should be able to represent these evaluations yielding model validity framework must be capable of representing the
validity. We consulted two sources to identify a population of validities used to evaluate these artifacts.
relevant papers against which to sample. First, we used the
MIS Quarterly Vol. 49 No. 4 / December 2025 1283
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Table 6. Validity Definitions (shaded cells indicate “not applicable”)
Name Part Output Artifact STS
Design science validity
Criterion validity
Criterion efficacy validity 19
Predictive validity 3
Concurrent validity 4
Criterion characteristic validity
Instance validity 0 0 5
Theory validity 0 0 0
Model validity 0 0 0
Method validity 0 0 10
Causal validity
Causal efficacy validity 24
Causal characteristic validity 7 0 1
Context validity
External validity 7
Ecological validity 1
Claim 3 is that the validity framework is complete in stated to be a validity or a concept not stated as such but listed
representing design science validity types, not only for with validity types (e.g., mundane realism as closely related
information systems but also for behavioral science, to ecological validity). We did not question the authors’
engineering, and medicine—when these disciplines are statements. In each case, we recorded new candidate validity
validating claims about their artifacts. By evaluating the types. In total, 2,418 candidate validity types emerged from
criterion claim that the framework is complete in its ability to approximately 7,500 manually examined sources. They were
represent design science validity definitions, we establish categorized by name before each category set was examined
model validity. By showing that our framework applies to to find homonyms (same name but different meaning),
other disciplines, we establish external validity. yielding 418 distinct validity types. This literature review was
used to generate the first version of the design science validity
The first task was to identify the specific design science framework.
validity types already proposed in the literature. No sizeable
existing set of general validity types was found. We thus built In the third task, we examined all articles published in the AIS
such a dataset for further refinement of a subset of validity Basket of Eight journals (Lowry et al., 2013) from 1994
types. We started by identifying and collecting validity types through 2017. A total of 6,083 articles were analyzed by
and definitions from various fields, including social sciences, applying 216 regular expression queries representing validity,
engineering and computer science, and medicine. This was reliability, and related concepts such as generalizability,
compiled over a three-year period by the first author and a which yielded 73,365 sentences. Sentences were ordered by
team of research assistants. The initial sources were the number of hits, with 9,707 sentences containing more than
documents containing sets of validity types, such as the two hits on the regular expressions manually examined by the
standards for educational and psychological testing (e.g., first author. This analysis only yielded 23 additional validity
American Educational Research Association et al., 2014). types, for a total of 441 candidate validity types, suggesting
The largest collection of validity names, 168, was provided by that the original process had been thorough. We removed from
Newton and Shaw (2014). The vast majority of these were in further evaluation any candidate validity type not in common
a large table as an exhibit of the intractable nature of validity use for which we failed to locate five definitions from
types. Still, many did not appear in any available database and different sources. One hundred and fifty-eight candidate
could not be found using a search engine. validity types were removed in this step.
The second task was to obtain definitions for the identified During the fourth task, the first and second authors
validity types. We relied primarily on scientific books and independently read the five definitions for each validity type
articles. For every source, the section containing the validity and selected one or two definitions that represented the overall
was further examined to identify more candidate validity aspects expressed by the other definitions. The decisions were
types. A candidate validity is a concept that the author either discussed (and recorded), and disagreements were resolved to
1284 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
obtain agreement on one or two definitions to represent the from behavioral science outlets, 37 (53%) from engineering
validity type. Because there were many cases where highly and computer science, and 10 (14%) from medicine; 22 (31%)
similar or even identical validity types existed, calculating were drawn from the sample of IS journals.
interrater reliability metrics was not appropriate. Eleven
candidate validity types were eliminated in this step because The first and third authors independently coded all validity
they did not fit our definition of a research validity (for definitions into the framework and agreed on 79.2% of cases
example, law-based validities) or because a clear definition (Cohen’s kappa = 0.731), which included cases of partial
had not emerged.9 agreement coded as non-agreement (for example, criterion
efficacy validity vs. predictive validity). Disagreements were
For the fifth task, with a final set of validity types specified, discussed and resolved. All definitions fit into a validity
the first and second authors followed our established category of the framework (left column of Table 7).10
definition of design science validity and independently coded
all validity types as “design science validity type” or “other
Thus, the evaluation yielded strong evidence for the validity
validity type.” The coders reached a 90.4% agreement with a
of Claim 3 in terms of both the criterion claim and the context
Cohen’s kappa of 0.79. The coders discussed and resolved any
claim, strengthening model validity, and providing external
disagreements. Almost all disagreements stemmed from the
validity. It did not support the need for the two causal validities
efficacy validity types, where one coder employed a more
included in the framework. However, our evaluation above in
inclusive interpretation. In total, 79 design science validity
the section on Claim 2 establishes the need for the causal
types were found.
validity types. The lack of attention to causal validity in the
existing validity type definitions suggests an opportunity to
From the design science validity types, we removed non-leaf
contribute to design science validity and, in turn, evaluation.
validity types, which combined multiple other validity types.
In this sense, it supports the need for templates in design
After removing these validity types, 70 definitions remained
for categorization in our framework. Of these, 23 (33%) came science, as proposed by Peffers et al. (2008).
Table 7. Validity Definition Coding
Design science validity Validities in the literature
Criterion validity
Criterion efficacy validity Absolute validity, criterion group validity, criterion validity, criterion-oriented validity,
criterion-related validity, decision validity, diagnostic validity, discriminative validity,
empirical validity, lower-order validity, operational validity, pragmatic validity,
procedural validity, postdictive validity, replicative validity, retrospective validity,
application validity
Predictive validity Predictive criterion validity, predictive validity (2)*, predictive criterion-related
validity
Concurrent validity Concurrent criterion validity, concurrent criterion-related validity, concurrent validity,
cross-sectional validity, relative validity
Criterion characteristic validity
Instance validity Observational validity, physical validity
Theory validity Aetiological validity, theoretical validity, instantiation validity
Model validity Conceptual model validity, functional validity, structural validity, semantic validity
Method validity Algorithmic validity, consistency
Causal validity
Causal efficacy validity
Causal characteristic validity
Context validity
External validity Pragmatical validity
Ecological validity Behavioral validity, ecological validity
Note: *Two slightly different versions of predictive validity referencing the same validity type.
9 Justification for each removal is available in the transparency materials. alarm, false discovery proportion, false negative, false negative rate, false
10 Validity metrics were included in the analysis, but because they do not omission rate, false positive, false positive rate, hit, hit rate, Matthews
employ a claim, they are not themselves validities. We therefore excluded correlation coefficient, miss, miss rate, negative predictive value, positive
the following metrics from classification: accuracy, area under the curve, predictive value, precision, recall, sensitivity, specificity, true negative, true
completeness, correct rejection, detection rate, F1-score, fall-out, false negative rate, true positive, and true positive rate.
MIS Quarterly Vol. 49 No. 4 / December 2025 1285
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Claim 4: The Causal Claim That the Framework categorized as “requirement validities.” In most cases, the
Is Parsimonious initial evaluation focused on terms such as “requirement” or
“satisfaction” and “acceptability.” Often, the evaluations were
The design science validity framework was developed poorly described by the original authors and unclear in terms
iteratively, as is common in design science. As we wanted to of the actual reference artifact or sociotechnical system. In this
remain inclusive, the initial version of the framework was causal validity evaluation, we focused on what we believed
more extensive than the one reported in this article. For the researchers considered to be their reference artifact. For
example, the initial framework contained a validity type the seven evaluations, we found five cases of model validity
termed “requirement validity”—a type of criterion and two cases of instance validity.
characteristic validity employed when comparing an artifact
to a requirements document or a user’s expectations and Thus, this evaluation showed that the validity framework
experience. However, requirements are not design science could be made more parsimonious without losing
artifacts that capture contributions to science and society, and representational capability. As such, the counterfactual
we were unable to clearly classify requirements validity as a evaluation for causal validity demonstrated that the removed
distinct validity type. We therefore engaged in a causal parts of the framework were not causally implicated in the
characteristic validity evaluation to examine the need for this performance of the framework. The other validity types were
validity type (supporting the claim that our framework without all built around the commonly acknowledged artifact types
this validity type is parsimonious and has no more and were necessary to classify the evidence, suggesting causal
components than needed). characteristic validity for the original claim of parsimony for
the remaining parts of the framework. Therefore, it is unlikely
Requirement validity was introduced to address knowledge that additional causal validity evaluations would enable the
claims against explicit requirements (e.g., function, ease of removal of additional parts. As a result, no further iterations
use, form) and implicit requirements (e.g., needs, goals, or were deemed necessary.
experiences with a similar class of artifacts). Requirement is a
common artifact produced in software development. Still, it
does not feature on common lists of design science artifact
Discussion and Implications
types (e.g., Gregor & Hevner, 2013; March & Smith, 1995).
However, we initially considered it to be a major reference
This research contributes to validity in design science that
entity of our framework, erring on the side of being more
could be expanded to other applications. There are both
inclusive and conservative. As our understanding of the
theoretical and practical implications of our work.
validity domain expanded over time, we began to question
whether requirement was needed. We choose to resolve this
issue by making a formal claim that requirement is a necessary
General Contributions
validity type for the framework to be complete.
A critical part of design science is validating knowledge
To validate this claim, we chose an evaluation approach based
claims about the focal artifacts. This research articulates why
on counterfactual reasoning. The first and the third authors
validation procedures are needed and provides a process by
cooperatively coded two validity definitions previously coded
which they can be identified and enacted through various
as “requirement validity” in the original framework. First, we
validity types.
examined “application validity,” defined as whether a
simulation model corresponds to its purpose and
We propose the design science validity framework. It maps
requirements; i.e., the likelihood that the model produces
validity types to characteristics of knowledge claims, aiding
outputs that reflect some external artifact or sociotechnical
authors in formulating and communicating their knowledge
system. Based on our improved understanding of the
claims and the evidence supporting them. Based on the
framework, this validity instance was recoded as a criterion
largest-ever review of validity literature, the design science
efficacy validity. The second existing definition was “semantic
validity framework is a comprehensive framework for
validity,” defined in part based on the appropriateness of the
validating knowledge claims about artifacts. The framework
category definitions. We realized that the reference entity was
provides a standard vocabulary for research validity reporting.
the semantic evaluators’ understanding of an equivalent
It has external validity in that it successfully represents all
model or sociotechnical system category, suggesting that this
identified artifact-related validity evidence from information
was a model validity. The same logic became clearer when
systems, behavioral science, engineering, computer science,
examining seven design science evaluations initially
and medicine.
1286 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
The framework guides researchers in identifying the knowledge claims in experimentation). However, psychometric validities
claims about artifacts by considering the branches of the are insufficient to support the range of knowledge claims in a
hierarchy of validity types, thus strengthening the rigor and design science project.
contribution of design science projects. By providing a process
and nomenclature for validating knowledge claims, the Finally, as confirmed in our applicability check, a major
framework can be applied to any type of artifact creation and challenge for researchers who create artifacts lies in the
evaluation. Explicitly connecting validity types, evaluation uncertain nature of validation and the tendency to perform
processes, and supporting evidence to knowledge claims should validation activities implicitly with little sense of the underlying
be useful for researchers and reviewers in design science, as structure of such validations. The validity framework provides
well as for those adopting other research approaches. Hence, researchers with a structured template and a set of carefully
our framework can help forge ties between design science and explained validity types with explicit, standardized definitions.
other types of research. The explicated knowledge claims can The validation process allows researchers to gather evidence
also be used to extend contributions in prior work. This could that supports a validity type explicitly connected to a knowledge
be done, for example, by making causal and context claims claim about a designed artifact.
about the artifacts or adding additional criterion claims with
more recent comparison entities.
Practical Suggestions
Findings and Implications Summarizing the arguments and findings of our paper, we
make the following recommendations for researchers who
Constructing and evaluating the design science validity are interested in developing artifacts to contribute to science
framework led to several notable insights that demonstrate its and society.
value. First, design scientists have historically used ad hoc
evaluations to support implicit claims about the validity of the State knowledge claims explicitly: To attain high levels of
artifact itself. To center and broaden validity as an aspect of practical utility and scientific replicability, researchers
rigor in design science, we shift these evaluations to should explicate knowledge claims about their artifacts. This
establishing the validity of explicit knowledge claims about can help frame research contributions and guide validation
the artifact. These claims will have varying degrees of because validation depends on articulated knowledge
supporting evidence, the sufficiency of which will be claims. In addition, explicit knowledge claims support the
established by the community and potentially contested and accumulation of knowledge.
changed over time.
Given that design knowledge can evolve through iterative
Second, there is a surprising lack of comprehensive discussion refinement of an artifact (Tuunanen et al., 2024), claims can
of design science validity, even though the evaluations and emerge at various stages during iterations. For example,
types of validity are well-established and understood in other some claims can be made prior to the development of an
disciplines. Published design science uses a narrow range of
artifact, while others can be made after deploying an artifact
validity concepts, largely focusing on efficacy measures and
in some context and observing outcomes. However, the latter
characteristic validity types, suggesting that validity has been
claims should not be considered validated until they have
underutilized. In our review of the literature, the most
undergone an appropriate validation procedure, possibly in
frequently occurring terms were accuracy, precision, recall,
a subsequent iteration of the artifact. What is important is
specificity, true positive, and false positive (concepts related
that a knowledge claim is formally evaluated independently
to the confusion matrix). These are, in fact, metrics rather than
of the process that generated the claim, which requires that
validity types, but are used in establishing efficacy validity. In
claims be stated explicitly.
the sample of publications analyzed, these validity metrics
were most frequently related to the evaluation of machine
Make claims commensurate with the intended
learning models, which, of course, does not represent the
contribution: The design science validity framework should
scope of design science.
not be used to justify excessive validations. It may be
impossible/unnecessary to state every claim about the artifact.
Third, some validity types used in design science have been
Further, in some cases (e.g., due to the difficulty of performing
adopted from other disciplines. However, this does not
comparisons or acquiring suitable comparison entities) not all
facilitate a holistic evaluative approach for design science. For
relevant claims can be subjected to validation. The question of
example, validity in psychometrics and econometrics is
how much evidence is necessary depends on the context and
strongly focused on measurement, and some types are useful
specific characteristics of a problem.
in design science (e.g., internal validity to support causality
MIS Quarterly Vol. 49 No. 4 / December 2025 1287
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Researchers should make at least one criterion claim about the procedures for these validity types. As the community
artifact, striving to make comparisons against state-of-the-art continues to apply and refine these validity types, their
artifacts or processes. This may be sufficient if the artifact is robustness is expected to grow, giving researchers a stronger
particularly novel, such that little is understood about what foundation on which to build their research.
makes it effective or about additional (beyond the original)
settings where it can be deployed. Beyond this, causal and The design science validity framework provides opportunities
context claims strengthen the research contribution because for future research. First, the framework is extensible, meaning
they deepen design knowledge and help practitioners reliably it can accommodate additional validity subtypes that might be
and safely apply the research findings in diverse settings. proposed by the research community (e.g., further refinement
of model validity based on types of models). Second, it is
Ensure every knowledge claim is validated: If an original possible to better track patterns of validation in design science
claim about an artifact is formulated, it should be validated. and identify gaps and opportunities (e.g., the need for more
For example, if some component of an artifact is claimed to context claims). A related possibility is improving validation
cause a specific outcome, then establishing causal validity is procedures by ensuring that appropriate validation practices are
appropriate. While a single validation does not prove a systematically captured for their respective validity types.
knowledge claim, validating claims increases the likelihood of Finally, researchers could investigate the applications of the
producing reliable design knowledge. framework in design science projects and report results related
to the usefulness and long-term impact of using the framework
As for how much evaluation is needed to establish the validity on the maturity of design science and its integration with other
of a claim, Galison and D’Agostino (1987) present a convincing research traditions.
argument that the sufficiency of evidence is a matter of
community agreement. The number of validation activities
required is commonly not based on a specific rule but on a Conclusion
consensus regarding the assembly of “persuasive arguments,
ones that will ‘stand up in court’” (Galison & D’Agostino, This research defines validity for design science and proposes
1987, p. 227). Researchers and review teams reach such the design science validity framework and a process for its use.
consensus during the review process. What is important is that The framework, derived from an extensive review and
the validation procedures undertaken are appropriate for analysis of the literature on validity, identifies and organizes
validating the knowledge claims made in a paper. implicit and explicit validity types into three main categories:
criterion, causal, and context. The validity categories are
Validate claims throughout the artifact journey: Many intended to assist researchers in rigorously obtaining and
artifacts emerge through iterative processes via presenting evidence of their knowledge claims. Mapping
experimentation, tinkering, or gradual improvement. Some knowledge claims onto the validity framework should support
projects involve multiple stages and produce different artifacts scholars and help connect the scientific knowledge related to
during these stages (e.g., conceptual model, system prototype, information systems artifacts. The framework itself was
beta version, final system in production) (Tuunanen et al., validated by evaluating its own knowledge claims and
2024). Knowledge claims about the resulting artifacts can be providing evidence for the relevant validity types that support
made throughout this process. Formative validation of these those claims.
claims can help in further artifact refinement and
improvement. The “intermediate” validations can be informal,
such as using a convenience sample of prospective users or an Acknowledgements
easy-to-obtain criterion. However, to ensure that the resulting
artifact reliably contributes to science and practice, the claims The authors wish to thank the senior editor, Balaji Padmanabhan, the
about the final or public version of the artifact should be associate editor, Stefan Seidel, and the anonymous reviewers for their
subject to rigorous summative validation.
work on prior versions of our paper. We appreciate the feedback
received from participants at workshops at HICSS, ECIS, the
University of Colorado Boulder, the University of Arizona, Arizona
Ensure appropriate validity types are used: A researcher
State University, and the University of Sydney, and the Technical
can refer to the design science validity framework during the University of Dresden. This research was supported in part by
validation of their knowledge claims. The framework organizes funding from the U.S. National Institutes of Health to Kai R. Larsen
diverse validity practices into a coherent reference system. It (Grant 3U24AG052175-08S1) and by funding from the Natural
shows what validity types are appropriate for each claim type Sciences and Engineering Council of Canada to Jeffrey Parsons
and suggests reasonable comparison entities and comparison (Grant RGPIN-2020-04916).
1288 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
References Collins, J., Hall, N., & Paul, L. A. (2004). Causation and
counterfactuals. MIT Press.
Cook, T. D., & Campbell, D. T. (1979). Quasi-experimentation: Design
Abbasi, A., Albrecht, C., Vance, A., & Hansen, J. (2012). MetaFraud:
& analysis issues for field settings. Rand McNally.
A meta-learning framework for detecting financial fraud. MIS
Creswell, J. W., & Miller, D. L. (2000). Determining validity in
Quarterly, 36(4), 1293-1327. https://doi.org/10.2307/41703508
qualitative inquiry. Theory into Practice, 39(3), 124-130.
Abbasi, A., & Chen, H. (2008). CyberGate: A design framework and
https://doi.org/10.1207/s15430421tip3903_2
system for text analysis of computer-mediated communication.
Cronbach, L. J., & Meehl, P. E. (1955). Construct validity in
MIS Quarterly, 32(4), 1-30. https://doi.org/10.2307/25148873
psychological tests. Psychological Bulletin, 52(4), 281-302.
Abbasi, A., Zhou, Y., Deng, S., & Zhang, P. (2018). Text Analytics to
https://doi.org/10.1037/h0040957
Support Sense-Making in Social Media: A Language-Action
Ethayarajh, K., & Jurafsky, D. (2020). Utility is in the eye of the user:
Perspective. MIS Quarterly, 42(2), 1-38. https://doi.org/10.25300/
A critique of NLP leaderboards. arXiv. https://doi.org/
MISQ/2018/13239
10.48550/arXiv.2009.13888
American Educational Research Association, American Psychological
Etudo, U., Yoon, V., & Liu, D. (2017). Financial concept element
Association, National Council on Measurement in Education, Joint
mapper (FinCEM) for XBRL interoperability: Utilizing the M3
Committee on Standards for Educational, & Psychological Testing
Plus method. Decision Support Systems, 98, 36-48.
(US). (2014). Standards for educational and psychological testing.
https://doi.org/10.1016/j.dss.2017.04.006
Amer Educational Research Assn.
Fan, W., Liu, X., Lu, P., & Tian, C. (2018). Catching numeric
Arazy, O., Kumar, N., & Shapira, B. (2010). A theory-driven design
inconsistencies in graphs. In Proceedings of the 2018 International
framework for social recommender systems. Journal of the
Conference on Management of Data (pp. 381-393).
Association for Information Systems, 11(9), 455-490.
https://doi.org/10.1145/3183713.3183753
https://doi.org/10.17705/1jais.00237
Galison, P. L., & D’Agostino, S. (1987). How experiments end.
Avdiji, H., & Winter, R. (2019). Knowledge gaps in design science
University of Chicago Press Chicago.
research. In DESRIST Proceedings.
Germonprez, M., Hovorka, D., & Collopy, F. (2007). A theory of
Avoine, G., Bingol, M. A., Kardas, S., Lauradoux, C., & Martin, B.
tailorable technology design. Journal of the Association for
(2009). A formal framework for cryptanalyzing RFID distance
Information Systems, 8(6), 351-367. https://doi.org/10.17705/
bounding protocols. Cryptology ePrint Archive, 2009:543.
1jais.00131
Baskerville, R., Kaul, M., & Storey, V. C. (2015). Genres of inquiry in
Gonzalez-Huerta, J., Boubaker, A., & Mili, H. (2017). A business
design-science research: Justification and evaluation of knowledge
process re-engineering approach to transform BPMN models to
production. MIS Quarterly, 39(3), 541-564. https://doi.org/
software artifacts. In E. Aïmeur, U. Ruhi, et al. (Eds.), Lecture
10.25300/MISQ/2015/39.3.02
Notes in Business Information Processing (Vol. 289, pp. 170–184).
Boudreau, M.-C., Gefen, D., & Straub, D. W. (2001). Validation in
Springer. https://doi.org/10.1007/978-3-319-59041-7_10
information systems research: A state-of-the-art assessment. MIS
Gregor, S., & Hevner, A. R. (2013). Positioning and presenting design
Quarterly, 25(1), 1-16. https://doi.org/10.2307/3250956
science research for maximum impact. MIS Quarterly, 37(2), 337-
Burton-Jones, A., Boh, W. F., Oborn, E., & Padmanabhan, B. (2021).
355. https://doi.org/10.25300/MISQ/2013/37.2.01
Editor’s comments: Advancing research transparency at MIS
Gregor, S., & Jones, D. (2007). The anatomy of a design theory.
Quarterly: A pluralistic approach. MIS Quarterly, 45(2), iii-xviii.
Journal of the Association for Information Systems, 8(5), 312-335.
https://doi.org/10.25300/MISQ/2021/452E1
https://doi.org/10.17705/1jais.00129
Carter, J. W. (2019). Aristotle on earlier Greek psychology: The
Gregor, S., Kruse, L. C., & Seidel, S. (2020). The anatomy of a design
science of soul. Cambridge University Press.
principle. Journal of the Association for Information Systems,
Chan, E. K. (2014). Standards and guidelines for validation practices:
21(6), 1622-1652. https://doi.org/10.17705/1jais.00649
Development and evaluation of measurement instruments. In B.
Gregory, R. W., & Muntermann, J. (2014). Research note—Heuristic
Zumbo & E. Chan (Eds.), Validity and validation in social,
theorizing: Proactively generating design theories. Information
behavioral, and health sciences (pp. 9-24). Springer.
Systems Research, 25(3), 639-653. https://doi.org/10.1287/isre.
https://doi.org/10.1007/978-3-319-07794-9_2
2014.0533
Chatterjee, S., Sarker, S., Lee, M. J., Xiao, X., & Elbanna, A. (2021).
Guba, E. G., & Lincoln, Y. S. (1994). Competing paradigms in
A possible conceptualization of the information systems (IS)
qualitative research. K. Denzin & Y. S. Lincoln (Eds.), Handbook
artifact: A general systems theory perspective. Information
of qualitative research (pp. 105-117). SAGE.
Systems Journal, 31(4), 550-578. https://doi.org/10.1111/isj.12320
Gumport, P. J. (2007). Sociology of higher education: Contributions
Chowdary, G. J., & Kanhangad, V. (2022). A dual-branch network for
and their contexts. Johns Hopkins University Press + ORM.
diagnosis of thorax diseases from chest X-rays. IEEE Journal of
Hevner, A., March, S., Park, J., & Ram, S. (2004). Design science in
Biomedical and Health Informatics, 26(12), 6081-6092.
information systems research. MIS Quarterly, 28(1), 75-105.
https://doi.org/10.1109/JBHI.2022.3215694
https://doi.org/10.2307/25148625
Cohen, L., Manion, L., & Morrison, K. (2013). Research methods in
Hevner, A., Parsons, J., Brendel, A. B., Lukyanenko, R., Tiefenbeck,
education. Routledge.
V., Tremblay, M. C., & vom Brocke, J. (2024). Transparency in
Collier-Reed, B., & Ingerman, Å. (2013). Phenomenography: From
design science research. Decision Support Systems, 182(1), 1-19.
critical aspects to knowledge claim. In Phenomenography: From
https://doi.org/10.1016/j.dss.2024.114236
critical aspects to knowledge claim. In J. Huisman & M. Tight
Hoyningen-Huene, P. (2013). Systematicity: The nature of science.
(Eds.), Theory and method in higher education research (Vol. 9,
Oxford University Press.
pp. 243-260). Emerald. https://doi.org/10.1108/S1479-3628(2013)
Iivari, J. (2015). Distinguishing and contrasting two strategies for
0000009016
design science research. European Journal of Information Systems,
24(1), 107-115. https://doi.org/10.1057/ejis.2013.35
MIS Quarterly Vol. 49 No. 4 / December 2025 1289
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Iivari, J., Rotvit Perlt Hansen, M., & Haj-Bolouri, A. (2021). A Moules, N. J., McCaffrey, J., & Field, J. (2015). Conducting
proposal for minimum reusability evaluation of design principles. hermeneutic research: From philosophy to practice. Peter Lang.
European Journal of Information Systems, 30(3), 286-303. Murray-Smith, D. J. (2015). Testing and validation of computer
https://doi.org/10.1080/0960085X.2020.1793697 simulation models: Principles, methods and applications.
Johannesson, P., & Perjons, E. (2014). An introduction to design Springer.
science. Springer. National Academies: Sciences, Engineering, and Medicine. (2022).
Koornneef, H., Verhagen, W. J., & Curran, R. (2020). A decision Ontologies in the behavioral sciences: Accelerating research and
support framework and prototype for aircraft dispatch assessment. the spread of knowledge: Digest version. The National Academies
Decision Support Systems, 135, Article 113338. https://doi.org/ Press.
10.1016/j.dss.2020.113338 Newell, A. (1975). A tutorial on speech understanding systems. In J.
Kuechler, W., & Vaishnavi, V. (2012). A framework for theory Wolf (Ed.), Speech recognition: Invited papers presented at the
development in design science research: Multiple perspectives. 1974 IEEE Symposium (pp. 3-54). Academic Press.
Journal of the Association for Information Systems, 13(6), 395- Newton, P., & Shaw, S. (2014). Validity in educational and
423. https://doi.org/10.17705/1jais.00300 psychological assessment. SAGE
Larsen, K., & Bong, C. H. (2016). A tool for addressing construct Nunamaker, J. F., Chen, M., & Purdin, T. D. (1991). Systems
identity in literature reviews and meta-analyses. MIS Quarterly, development in information systems research. Journal of
40(3), 529-551. https://doi.org/10.25300/MISQ/2016/40.3.01 Management Information Systems, 7(3), 89-106.
Larsen, K. R., & Becker, D. S. (2020). Automated machine learning Onwuegbuzie, A. J., & Leech, N. L. (2007). Validity and qualitative
for business: An introduction to accurate, easy, and fast analytics. research: An oxymoron? Quality & Quantity, 41(2), 233-249.
Oxford University Press. https://doi.org/10.1080/07421222.1990.11517898
Larsen, K. R., Hovorka, D., Dennis, A., & West, J. D. (2019). Pääkkönen, T., Kekäläinen, J., Keskustalo, H., Azzopardi, L., Maxwell,
Understanding the elephant: The discourse approach to boundary D., & Järvelin, K. (2017). Validating simulated interaction for
identification and corpus construction for theory review articles. retrieval evaluation. Information Retrieval Journal, 20, 338-362.
Journal of the Association for Information Systems, 20(7), 887- https://doi.org/10.1007/s10791-017-9301-2
927. https://doi.org/10.17705/1jais.00556 Padmanabhan, B., Fang, X., Sahoo, N., & Burton-Jones, A. (2022).
Li, J., Larsen, K. R., & Abbasi, A. (2020). TheoryOn: A design Machine learning in information systems research. MIS Quarterly,
framework and system for unlocking behavioral knowledge 46(1), iii-xix. https://doi.org/10.25300/MISQ/2022/461E1
through ontology learning. MIS Quarterly, 44(4), 1733-1772. Peffers, K., Tuunanen, T., & Niehaves, B. (2018). Design science
https://doi.org/10.25300/MISQ/2020/15323 research genres: Introduction to the special issue on exemplars and
Lincoln, Y. S., & Guba, E. G. (1985). Naturalistic inquiry. SAGE. criteria for applicable design science research. European Journal
Lowry, P. B., Gaskin, J., Humpherys, S. L., Moody, G. D., Galletta, D. of Information Systems, 27(2), 129-139. https://doi.org/10.1080/
F., Barlow, J. B., & Wilson, D. W. (2013). Evaluating journal 0960085X.2018.1458066
quality and the Association for Information Systems Senior Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S.
Scholars’ Journal Basket via bibliometric measures: Do expert (2008). A design science research methodology for information
journal assessments add value? MIS Quarterly, 37(4), 993-1012. systems research. Journal of Management Information Systems,
https://doi.org/10.25300/MISQ/2013/37.4.01 24(3), 45-77. https://doi.org/10.2753/MIS0742-1222240302
Lukyanenko, R., & Parsons, J. (2020). Design theory indeterminacy: Piramuthu, S., & Doss, R. (2017). On sensor-based solutions for
What is it, how can it be reduced, and why did the polar bear simultaneous presence of multiple RFID tags. Decision Support
drown? Journal of the Association for Information Systems, 21(5), Systems, 95, 102-109. https://doi.org/10.1016/j.dss.2017.01.003
1-30. https://doi.org/10.17705/1jais.00639 Prat, N., Comyn-Wattiau, I., & Akoka, J. (2015). A taxonomy of
Lukyanenko, R., Parsons, J., Wiersma, Y., & Maddah, M. (2019). evaluation methods for information systems artifacts. Journal of
Expecting the unexpected: Effects of data collection design choices Management Information Systems, 32(3), 229-267.
on the quality of crowdsourced user-generated content. MIS https://doi.org/10.1080/07421222.2015.1099390
Quarterly, 43(2), 634-647. https://doi.org/10.25300/MISQ/2019/ Ramakrishnan, M., Gregor, S., Shrestha, A., & Soar, J. (2023). Design
14439 principles for platform-enabled knowledge commons with an
Mandviwalla, M. (2015). Generating and justifying design theory. expository instantiation. Journal of the Association for Information
Journal of the Association for Information Systems, 16(5), 314- Systems, 24(5), 1413-1438. https://doi.org/10.17705/1jais.00824
344. https://doi.org/10.17705/1jais.00397 Refsgaard, J. C., Van der Sluijs, J. P., Brown, J., & Van der Keur, P.
March, S. T., & Smith, G. F. (1995). Design and natural science (2006). A framework for dealing with uncertainty due to model
research on information technology. Decision Support Systems, structure error. Advances in Water Resources, 29(11), 1586-1597.
15(4), 251-266. https://doi.org/10.1016/0167-9236(94)00041-2 https://doi.org/10.1016/j.advwatres.2005.11.013
Matadamas-Hernández, J., Román-Alonso, G., Rojas-González, F., Roberts, P., & Priest, H. (2006). Reliability and validity in research.
Castro-García, M. A., Boukerche, A., Aguilar-Cornejo, M., & Nursing Standard, 20(44), 41-46. https://doi.org/10.7748/ns2006.
Cordero-Sánchez, S. (2012). Parallel simulation of pore networks 07.20.44.41.c6560
using multicore CPUs. IEEE Transactions on Computers, 63(6), Rosemann, M., & Vessey, I. (2008). Toward improving the relevance
1513-1525. https://doi.org/10.1109/TC.2012.197 of information systems research to practice: The role of
Maxwell, J. (1992). Understanding and validity in qualitative research. applicability checks. MIS Quarterly, 32(1), 1-22. https://doi.org/
Harvard Educational Review, 62(3), 279-301. https://doi.org/ 10.2307/25148826
10.17763/HAER.62.3.8323320856251826 Salmon, W. C. (1998). Causality and explanation. Oxford University
Meth, H., Mueller, B., & Maedche, A. (2015). Designing a requirement Press.
mining system. Journal of the Association for Information Systems, Sedrakyan, G., Poelmans, S., & Snoeck, M. (2017). Assessing the
16(9), 799-837. https://doi.org/10.17705/1jais.00408 influence of feedback-inclusive rapid prototyping on
1290 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
understanding the semantics of parallel UML statecharts by novice About the Authors
modellers. Information and Software Technology, 82, 159-172.
https://doi.org/10.1016/j.infsof.2016.11.001
Kai R. Larsen is a professor of information systems in the Leeds
Sein, M., Henfridsson, O., Purao, S., Rossi, M., & Lindgren, R. (2011).
School of Business, University of Colorado Boulder. He is a courtesy
Action design research. MIS Quarterly, 35(1), 37.
https://doi.org/10.2307/23043488 faculty member in the Department of Information Science, a professor
Shultz, K. S., Riggs, M. L., & Kottke, J. L. (1998). The need for an at the University of Agder, and a research advisor to Gallup. Kai is most
evolving concept of validity in industrial and personnel known for providing a practical solution to Edward Thorndike’s (1904)
psychology: Psychometric, legal, and emerging issues. Current jingle fallacy and for his contributions to the semantic theory of survey
Psychology, 17, 265-286. https://doi.org/10.1007/s12144-998- response (STSR). He received the INFORMS Design Science Award
1011-x for 2019, the Herbert A. Simon Design Science Award for 2020, and
Taylor, C. S. (2013). Validity and validation. Oxford University Press. the AIS Education Innovation Award for 2023. ORCiD: 0000-0002-
Thomas, M. A., Li, Y., & Lee, A. S. (2022). Generalizing the
8812-9866
information systems artifact. Information Systems Research, 33(4),
1452-1466. https://doi.org/10.1287/isre.2022.1106
Roman Lukyanenko is an associate professor at the McIntire School
Tiefenbeck, V., Goette, L., Degen, K., Tasic, V., Fleisch, E., Lalive, R.,
of Commerce, University of Virginia. His research interests include
& Staake, T. (2016). Overcoming salience bias: How real-time
feedback fosters resource conservation. Management Science, data management and research methods (validity and artificial
64(3), 1458-1476. https://doi.org/10.1287/mnsc.2016.2646 intelligence in literature reviews). Roman’s ideas, tools, and methods
Tuunanen, T., Winter, R., & Vom Brocke, J. (2024). Dealing with to improve data management and research practices have received
complexity in design science research: A methodology using major awards, including the INFORMS Design Science Award, the
design echelons. MIS Quarterly, 48(2), 427-458. https://doi.org/ Governor General of Canada Gold Medal, and the Hebert A. Simon
10.25300/MISQ/2023/16700 Design Science Award. Roman’s research has been published in 140
Umapathy, K., Purao, S., & Barton, R. R. (2008). Designing enterprise
conferences and journals, including Nature, MIS Quarterly,
integration solutions: Effectively. European Journal of
Information Systems Research, and ACM Computing Surveys. His
Information Systems, 17(5), 518-527. https://doi.org/10.1057/ejis.
2019 paper on the quality of crowdsourced data received the Best Paper
2008.39
Award at MIS Quarterly. Roman is a co-author of “Systems Analysis
Valecha, R., Sharman, R., Rao, H. R., & Upadhyaya, S. (2013). A
and Design: An Object-Oriented Approach with UML” textbook
dispatch-mediated communication model for emergency response
systems. ACM Transactions on Management Information Systems, published by Wiley. ORCiD: 0000-0001-8125-5918
4(1), 1-25. https://doi.org/10.1145/2445560.2445562
Venable, J., Pries-Heje, J., & Baskerville, R. (2016). FEDS: a Roland M. Mueller is a professor of information systems at the Berlin
framework for evaluation in design science research. European School of Economics and Law in Germany. He earned his Ph.D. in
Journal of Information Systems, 25(1), 77-89. https://doi.org/ information systems from the Free University of Berlin. His research
10.1057/ejis.2014.36 interests include ontologies and large language models for literature
Venkatesh, V., Morris, M. G., Davis, G. B., & Davis, F. D. (2003). User
reviews, meta-theoretical analysis, ontology engineering, design
acceptance of information technology: Toward a unified view. MIS
science methods, and user-driven innovation in AI projects. He has
Quarterly, 27(3), 425-478. https://doi.org/10.2307/30036540
authored three books and over 100 academic papers, with his work
vom Brocke, J., Gau, M., & Mädche, A. (2021). Journaling the design
receiving multiple accolades, including the Herbert A. Simon Design
science research process. Transparency about the making of design
knowledge. In DESRIST Proceedings (pp. 131-136). https://doi. Science Award. Beyond academia, Roland has contributed to
org/10.1007/978-3-030-82405-1_15 innovation as a founder and advisory board member of several startups
vom Brocke, J., Hevner, A. R., & Maedche, A. (2020). Design science and holds a patent in machine learning. ORCiD: 0000-0002-8706-7763
research: Cases. Springer.
vom Brocke, J., Winter, R., Hevner, A., & Maedche, A. (2020). Veda C. Storey is a Distinguished University Professor, the Tull
Accumulation and evolution of design knowledge in design Professor of Computer Information Systems, and a professor of
science research: A journey through time and space. Journal of the
computer science at the J. Mack Robinson College of Business,
Association for Information Systems, 21(3), 520-544. https://doi.
Georgia State University. Her research interests are in data
org/10.17705/1jais.00611
management, conceptual modeling, and design science. She is
Weinhardt, C., Kloker, S., Hinz, O., & van der Aalst, W. M. (2020).
particularly interested in the assessment of the impact of new
Citizen science in information systems research. Business &
Information Systems Engineering, 62, 273-277. https://doi.org/ technologies on business and society from a data management
10.1007/s12599-020-00663-y perspective. Dr. Storey is a member of the AIS College of Senior
Winter, S., Berente, N., Howison, J., & Butler, B. (2014). Beyond the Scholars and the steering committee of the International Conference of
organizational “container”: Conceptualizing 21st century Conceptual Modeling. She is a recipient of the Peter P. Chen Award,
sociotechnical work. Information and Organization, 24(4), 250- an ER Fellow, an AIS Fellow, and an INFORMS Fellow. ORCiD:
269. https://doi.org/10.1016/j.infoandorg.2014.10.003 0000-0002-8753-1553
Zaitsev, A., & Mankinen, S. (2022). Designing financial education
applications for development: Applying action design research in
Jeffrey Parsons is a university research professor and professor of
Cambodian countryside. European Journal of Information
information systems in the Faculty of Business Administration at
Systems, 31(1), 91-111. https://doi.org/10.1080/0960085X.2021.
Memorial University of Newfoundland in Canada. His research
1978341
MIS Quarterly Vol. 49 No. 4 / December 2025 1291
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
interests focus on how to better represent human conceptualizations Dirk S. Hovorka is a professor in the business information systems
of the world in data. His work on this and related topics has been discipline at the University of Sydney, Australia. He received his
published in several disciplines. Jeff’s research has been Ph.D. in information systems from the University of Colorado
recognized in several ways, including the MIS Quarterly Paper of Boulder and holds an M.S. in interdisciplinary telecommunications
the Year Award (2019), the AIS Senior Scholars Paper Award and an M.S. in geology. His current research explores how
(2020), and the INFORMS Design Science Award (2014). He is a scientific and societal practices bring forth possible “worlds”
Fellow of the Association for Information Systems, Distinguished through theory, design, and conceptualizations of futures. His
Research Fellow from TU Dresden, Schoeller Senior Fellow, and research focuses on speculative approaches to “knowing”
an ER Fellow. He has served as a senior editor at the MIS Quarterly regarding technology, society, and biophysical environments in
and is currently a senior editor at Information Systems Research. recognition that the future is implacably resistant to empirical
ORCiD: 0000-0002-4819-2801 knowing and that unprecedented sociotechnical change renders our
knowledge about the past less indicative of future states. Dirk is a
Debra Vander Meer is a professor of information systems at senior editor at the Journal of the Association for Information
Florida International University (FIU). Her current research Systems (Research Perspectives) and an editorial board member at
interests focus on applying concepts from computer science and Information Systems Research, and co-chair of the HICSS
information systems to real-world problems. Her work appears in Informing Research: Engaging with Futures mini-track and the
premier journals and conferences in these areas. Prior to joining ECIS Future as a Site of Inquiry track. He has been awarded the
FIU, she spent a decade working in industry, including roles in a 2018 Beta Gamma Sigma Professor of the Year Award, the Wayne
venture-funded startup. She holds a bachelor’s degree from Lonergan Award for Outstanding Teaching (2018), and the Dean’s
Georgetown University, a master’s of science degree in Award for Teaching (2022) and has numerous Teaching Citations.
management information systems from the University of Arizona, Dirk is a co-author of the AIS 2011 Best Paper “Secondary Design:
and a doctoral degree in computer science from the Georgia A Case of Behavioral Design Research.” ORCiD: 0000-0001-
Institute of Technology. ORCiD: 0000-0002-5930-6667 7049-5617
1292 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

Larsen et al. / Validity in Design Science
Appendix
Overall Usage of Design Science Validity Types
We examined the extent to which the design science validity framework, translated into the existing 70 validity definitions sorted into our
framework in the right column of Table 7, were used in 199 design science papers published in the AIS Senior Scholars’ Basket of Eight
journals between April 2004 and December 2017. Each paper was examined at the sentence level and compared to our list of validity types,
using regular expressions at the word level. The first author read all resulting sentences and excluded search results where their regular
expressions yielded excessive false positives. For example, terms such as accuracy, completeness, precision, and recall have specific but
polysemous meanings in data quality and machine learning research. The remaining terms yielded tens of thousands of sentences, so the
reported results are conservative estimates.
We identified the number of times a validity corresponding to one in the framework (Table 7) was used at least once within a paper, organized
by year and validity type. We concluded that design science papers do not use the same validity terms used in other disciplines, except for
some used to describe metrics from the confusion matrix. The validity names associated with the characteristic validity types were seldom
employed. Even within the highly used category of efficacy validity types, most validity-related terms discussed stemmed from confusion
matrix measures in machine learning. Exceptions were in the use of method characteristic validity types, the next most used validity types
found in the design science literature.
We found a lack of consistency and a lack of actual use of validity terms in design science papers, which implies a significant opportunity
for improved communication of evaluation by greater consistency in language around explicit validity claims. Once researchers commit to
shared validity norms, communication and reporting consistency should improve.
MIS Quarterly Vol. 49 No. 4 / December 2025 1293
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026

1294 MIS Quarterly Vol. 49 No. 4 / December 2025
Downloaded from http://misq.umn.edu/misq/article-pdf/49/4/1267/19176/02_ma_10.25300_misq_2024_18064.pdf by guest on 19 March 2026