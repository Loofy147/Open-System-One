# Experimental Opportunity Protocol v0.2

Status: METHODOLOGY — OPEN / EXPERIMENTAL
Date: 2026-10-01

## 0. الغرض

هذا البروتوكول مخصص لاكتشاف ما إذا كانت مشكلة عملية صغيرة تستحق تدخلًا برمجيًا صغيرًا.

الهدف ليس إنتاج أكبر عدد من الأفكار، ولا إثبات القدرة على بناء MVP.

الهدف هو:

اكتشاف مشكلة
→ إثبات الألم
→ قتل البدائل
→ تحديد الفجوة
→ اختبار جدوى التدخل
→ بناء أقل MVP
→ كسره
→ اتخاذ قرار

أفضل مخرج ممكن هو عدم البناء إذا لم تبقَ حاجة كافية.

---

## 1. قواعد التشغيل الأساسية

### قاعدة 1 — Problem First
لا يبدأ البحث باسم أداة أو فئة منتج أو حل تقني.
البداية دائمًا مشكلة سلوكية/عملية محددة.

### قاعدة 2 — Evidence Before Commitment
لا يتحول وجود وصف أو شكوى إلى «مشكلة مثبتة» دون دليل مناسب.

### قاعدة 3 — Existing Solution Adversarial Search
لا يكفي البحث عن المنافسين المباشرين.

يجب البحث أيضًا عن:
- scripts
- shell commands
- libraries
- hidden features
- CI workflows
- workarounds
- documentation recipes
- commercial products
- features داخل أدوات أكبر
- طرق يدوية شائعة

### قاعدة 4 — Residual Pain
المشكلة لا تبقى مرشحًا لمجرد وجودها.

السؤال:
«ماذا يبقى بعد أفضل workaround متاح اليوم؟»

إذا زال الألم تقريبًا، يُقتل المرشح.

### قاعدة 5 — Action Delta
الفجوة يجب أن تنتج فعلًا جديدًا أو قرارًا مختلفًا.

القاعدة:
Without tool ≠ With tool
من حيث قرار عملي مهم.

إذا كانت الأداة لا تغير ما سيفعله المستخدم، فقيمتها موضع شك حتى لو كانت تقنية ومفيدة نظريًا.

### قاعدة 6 — Minimal Intervention
إذا بقي المرشح، لا نبني «المنتج الكامل».
نبني أصغر تدخل يمكنه اختبار الفرضية المركزية.

### قاعدة 7 — Execution Is Not Proof of Opportunity
نجاح الـMVP يثبت أن التنفيذ ممكن فقط.

ولا يثبت:
- حجم الألم
- الطلب
- novelty
- product-market fit
- جدوى المنتج المستقل

### قاعدة 8 — Oracle Integrity
كل اختبار يجب فحصه هو نفسه.
إذا كان الـtest oracle خاطئًا، فإن نجاح الاختبار لا قيمة له.

### قاعدة 9 — Negative Knowledge Is First-Class
لا تُمحى الأفكار المقتولة أو الاختبارات الفاشلة.
تُحفظ أسباب قتلها حتى لا نعيد اكتشاف نفس الطريق.

### قاعدة 10 — No Forced Success
الحكم قد يكون:
«لا نبني شيئًا.»
وهذا مخرج صالح.

---

## 2. دورة حياة المرشح

كل Problem Candidate يمر بالحالات:

DISCOVERED
→ EVIDENCE_CHECK
→ SOLUTION_AUDIT
→ RESIDUAL_PAIN_CHECK
→ GAP_ANALYSIS
→ ACTION_DELTA_CHECK
→ PREBUILD_KILL_TEST
→ BUILD_ALLOWED
→ MVP
→ ADVERSARIAL_VERIFY
→ POSTBUILD_REASSESSMENT
→ DECISION

وقد يُقتل في أي مرحلة.
لا توجد قاعدة تجعل كل مرشح يصل إلى MVP.

---

## 3. سجل المرشح

لكل مرشح نحتفظ بـ:

candidate_id
problem_statement
affected_user/context
discovery_date
sources[]
current_solutions[]
workarounds[]
residual_pain
gap_statement
action_delta
kill_tests[]
status
decision
evidence_refs[]
contradiction_refs[]
experiment_refs[]
artifact_refs[]
next_discriminating_action

---

## 4. سجل الدليل

كل ادعاء مهم يجب أن يمتلك provenance.

نستخدم حالات المعرفة:

ESTABLISHED
EXPERIMENTALLY_SUPPORTED
USER_REPORTED
INFERENCE
HYPOTHESIS
CONTRADICTED
UNKNOWN
OPEN

ولا يُرفع الادعاء من حالة إلى أخرى بمجرد تكرار الكلام.

لكل Evidence نسجل:

evidence_id
source
source_type
retrieved_or_executed_at
scope
claim_supported
claim_not_supported
limitations
artifact_ref

---

## 5. سجل الطريقة

لكل تجربة أو بحث يجب معرفة:

experiment_id
method
inputs
environment
command / procedure
expected observation
oracle
actual result
artifacts
date
revision

الغرض هو منع:
«أظن أننا اختبرنا هذا.»

بل يجب أن نعرف:
«ماذا اختُبر، وأين، وبأي طريقة، وبأي نتيجة.»

---

## 6. بوابة A — Reality

السؤال:
«هل المشكلة موجودة أصلًا؟»

نبحث عن أدلة من النوع المناسب.

مثال:
incident
issue
support case
reproducible failure
repeated workflow
measured cost
documented workaround

إذا بقي الدليل:
single anecdote
ambiguous complaint
marketing claim

فالحالة:
UNKNOWN

ولا يُبنى عليها.

---

## 7. بوابة B — Existing Solutions

نبحث من أربع زوايا:

Direct
حلول صممت للمشكلة نفسها.

Adjacent
أدوات تحقق معظم الوظيفة.

Embedded
ميزة موجودة داخل منتج أكبر.

Procedural
وصفة يدوية أو command قصير يحل المشكلة.

يجب تسجيل كل سبب للرفض.

مثال:
candidate killed
reason:
existing tool solves 90% of need
remaining gap not consequential

---

## 8. بوابة C — Residual Pain

نحوّل:

Problem

إلى:

Problem after current workaround

ويجب أن نجيب:
«ما الشيء الذي لا يزال يكلف المستخدم شيئًا؟»

مثل:
time
error probability
manual repetition
operational risk
hidden failure
irreversibility
coordination cost

إذا لم يظهر residual pain واضح:
KILLED

---

## 9. بوابة D — Gap

الفجوة يجب صياغتها بطريقة قابلة للنقض:

Current solution can do X.
It cannot reliably do Y under condition Z.
Users currently perform W manually / accept failure.
Minimal intervention could provide Y.

يُرفض:
«التجربة الحالية ليست جميلة.»

ويُقبل مثل:
«الأداة الحالية تكشف X، لكنها لا تكشف Y قبل وقوع الفشل.»

---

## 10. بوابة E — Action Delta

هذا أحد أهم عناصر v0.2.

نسأل:
«ماذا سيفعل المستخدم بشكل مختلف نتيجة الأداة؟»

الصيغة:

Before:
action A

After:
action B

مثال:

Before:
publish artifact

After:
abort because required file will be omitted

إذا لم يوجد Action Delta ذو أثر عملي:
OPEN → likely KILL

---

## 11. بوابة F — Pre-build Kill Test

قبل الكود نحدد:

kill_hypothesis
cheap_test
failure_condition

مثال:

Hypothesis:
existing shell workflow is sufficient.

Cheap test:
construct five representative cases.

Kill condition:
shell solution resolves all cases without meaningful extra work.

نجاح kill test يعني:
DO NOT BUILD

---

## 12. بناء الـMVP

إذا بقي المرشح فقط:

BUILD_ALLOWED

نحدد:

minimal input
minimal transformation
minimal output
minimal interface

ولا نضيف:

dashboard
authentication
cloud backend
AI layer
plugins

إلا إذا كانت ضرورية لاختبار الفرضية.

---

## 13. Verification Matrix

يجب أن يحتوي التحقق على:

| الفئة | الغرض |
|---|---|
| Normal | الوظيفة الأساسية |
| Boundary | الحدود |
| False Positive | منع الإنذارات الكاذبة |
| False Negative | منع الفشل الصامت |
| Malformed | تحمل المدخلات غير الصحيحة |
| Hostile | الحالات العدائية |
| Unsupported | إثبات حدود الأداة |
| Oracle Check | التحقق من صحة الاختبار نفسه |

كل نتيجة تحفظ، بما فيها الفشل.

---

## 14. معالجة الفشل

عند اكتشاف خطأ:

FAILURE DETECTED
→ classify:
- tool bug
- test bug
- oracle bug
- environment issue
- misunderstood requirement
- genuine hypothesis contradiction

ثم:

repair
→ rerun affected tests
→ preserve old result
→ record revision

لا نستبدل الدليل القديم وكأن الفشل لم يحدث.

---

## 15. Post-build Kill Test

بعد وجود أداة حقيقية، نعيد البحث عن:

simpler alternative
existing command
existing feature
embedded capability
low pain frequency
adoption friction
false-positive cost
false-negative cost
limited audience
platform dependency
lack of action delta

ونطرح سؤالًا واحدًا:

«هل امتلاك هذه الأداة أفضل عمليًا من عدم امتلاكها؟»

إذا لم نستطع الدفاع عن ذلك بالأدلة، لا نرفع الحكم.

---

## 16. مستويات الحكم النهائي

يجب اختيار حالة واحدة فقط:

FOLLOW_UP

الدليل قوي بما يكفي لاستمرار التجربة.

SMALL_TOOL

الأداة مفيدة بوضوح، لكن لم يثبت أنها تستحق منتجًا مستقلاً.

NEEDS_DECISIVE_EXPERIMENT

هناك فرضية رئيسية لم تُحسم.

NOT_WORTH_BUILDING

المشكلة حقيقية، لكن الحل المستقل لا يقدم قيمة كافية.

HYPOTHESIS_FAILED

الدليل أو التجربة ناقضت الفرضية المركزية.

---

## 17. سجل التعارضات

كل Contradiction يسجل ككيان مستقل:

contradiction_id
claim
previous_state
new_observation
conflicting_evidence
scope
resolution
resolution_status

ولا يُفترض أن يكون أحد الطرفين «أصح» فقط لأنه أحدث.

قد تكون النتيجة:

different scope
different environment
different version
different interpretation
actual contradiction

---

## 18. سجل النتائج السلبية

مثال:

candidate X
killed because:
existing tool Y covers the entire residual pain

candidate Y
killed because:
action delta = 0

candidate Z
MVP worked
but adoption cost > practical benefit

هذا السجل جزء من المعرفة الناتجة، وليس نفايات البحث.

---

## 19. سجل الـMethods

لأننا نريد مقارنة المنهج نفسه عبر الجولات، لكل Candidate نحتفظ أيضًا بـ:

discovery_method
search_method
competitor_search_method
kill_method
prototype_method
verification_method
oracle_method
reassessment_method

وهكذا نستطيع لاحقًا أن نسأل:

«أي أسلوب بحث ينتج مرشحين يعيشون أكثر؟»

وأيضًا:

«أي Kill Test يقتل الأفكار الوهمية أسرع؟»

---

## 20. تقييم المنهج نفسه

لا نقيس النجاح بعدد الأدوات المبنية.

نقيس:

Candidates
→ Killed Before Build
→ MVP Survivors
→ Action Changing MVPs

ونتابع خصوصًا:

premature-build rate
false-survival rate
oracle-failure rate
competitor-miss rate
post-build-kill rate
action-delta rate

الغاية ليست تحسين score.
الغاية اكتشاف أين يخطئ المنهج.

---

## 21. قاعدة إعادة التقييم

بعد عدد كافٍ من التجارب، نراجع:

What repeatedly survives?
What repeatedly gets killed?
Which evidence types mislead?
Which search methods miss existing solutions?
Which kill tests are too weak?
Which MVPs produce no action delta?

ثم نعدل البروتوكول نفسه.

أي:

Method
→ Experiments
→ Results
→ Contradictions
→ Method Revision

وهذا يعني أن المنهج نفسه كيان تجريبي، وليس حقيقة مفترضة.

---

## 22. قاعدة الحالة المعرفية

لا يسمح بالتعبير:
«الفكرة جيدة.»

بل:

Problem: ESTABLISHED
Residual pain: EXPERIMENTALLY_SUPPORTED
Gap: INFERENCE
Action delta: HYPOTHESIS
MVP: EXPERIMENTALLY_SUPPORTED
Standalone value: UNKNOWN

وهذا هو الشكل المفضل للتقرير.

---

## 23. سجل القرار

لكل Decision:

decision_id
decision
date
based_on[]
rejected_alternatives[]
known_uncertainties[]
next_discriminating_action

إذا تغير القرار:
DecisionRevision

ولا يُمحى القرار القديم.

---

## 24. قاعدة عدم التضخيم

لا يجوز:

small observation
→ broad claim

مثال:

"tool detected 4 risky repositories"

لا يتحول تلقائيًا إلى:

"developers need this tool"

ولا:

"there is a market"

إلا إذا وُجد دليل مستقل مناسب.

---

## 25. المخرجات المطلوبة من كل دورة

كل دورة بحث يجب أن تنتهي بـ:

Candidates discovered
Candidates killed
Survivors
Evidence
Contradictions
Experiments executed
Artifacts
Current unknowns
Decision
Next discriminating action
Method lessons

ليس مطلوبًا أن تنتهي بأداة.

إذا انتهت بـ:
12 candidates
12 killed

فهذه نتيجة مفيدة.

---

## 26. الوضع الحالي

هذا البروتوكول يُعتبر:

METHODOLOGY — OPEN / EXPERIMENTAL

وليس «منهجًا مثبتًا».

الجولات الحالية تشكل التجارب الأولى التي سنستخدمها لتحسينه:

DriftProbe
JSONWitness
ArtifactPreflight
SymlinkPreflight
Pathfit

والدليل الناتج منها يستخدم لتعديل الطريقة، لا لإثبات أنها مثالية.

---

## 27. قاعدة المتابعة

لكل دورة جديدة لا نبدأ بعبارة:
«ما الأداة التي سنبنيها؟»

بل:
«ما المشكلات التي تستحق أن نحاول قتلها أولًا؟»

ثم نتبع السجل حتى نصل إلى قرار.

هذا البروتوكول لا يفترض أن تكون النتيجة أداة.

يفترض أن تكون النتيجة معرفة أفضل عن أي تدخل يستحق أن يُبنى، ولماذا، وتحت أي شروط، وما الذي قد ينقض هذا الحكم لاحقًا.

---

## Operational Integration

هذا v0.2 يحكم أعمال Problem Kill السابقة واللاحقة، ويضيف إليها بوابات إلزامية:

Problem First
→ Evidence
→ Adversarial Solution Audit
→ Residual Pain
→ Gap
→ Action Delta
→ Pre-build Falsification
→ Minimal Intervention
→ Adversarial Verification
→ Post-build Reassessment
→ Decision Revision

ولا يُعتبر أي مرشح:
BUILD_ALLOWED
إلا إذا اجتاز Pre-build Kill Test المحدد له.

ولا يُعتبر أي MVP:
proof of opportunity

بل مجرد:
proof of execution

والـExperimental Winner الذي يُبنى بعد نجاة المرشح ليس إطلاقًا ولا MVP تجاريًا؛ هو Research Instrument للإجابة عن أسئلة النظام المتراكمة والتحقق المستقل منها.

تم ربط هذه القاعدة مباشرةً بمخرجات:
- Problem Kill Campaign
- Pre-Build Falsification
- Experimental Winner Contract
- CapabilityKernel
- Direct Impact Guard
- Agent Surface A0-A10 protocol
- evidence / contradiction / decision lineage

والمرجع المعرفي النهائي يبقى في السجلات القابلة لإعادة التحقق، لا في المحادثة وحدها.
