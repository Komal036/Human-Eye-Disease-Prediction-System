# recommendation.py
# Detailed clinical recommendations per OCT class

cnv = """
**For CNV (Choroidal Neovascularization)**

CNV refers to the growth of abnormal blood vessels beneath the retina, most commonly
associated with neovascular (wet) age-related macular degeneration (AMD). These vessels
leak fluid and blood, causing rapid central vision loss if untreated.

---

**Immediate Action**
- Seek **urgent evaluation by a retinal specialist** — CNV can cause irreversible vision
  loss within weeks if not treated promptly.

**Treatment Options**
- **Anti-VEGF Injections** *(First-line)*: Intravitreal injections of Ranibizumab
  (Lucentis), Aflibercept (Eylea), or Bevacizumab (Avastin) suppress abnormal vessel
  growth. Typically given monthly initially, then tapered based on response.
- **Photodynamic Therapy (PDT)**: Verteporfin activated by laser selectively destroys
  abnormal vessels — used as adjunct or in select cases.
- **Laser Photocoagulation**: Reserved for extrafoveal CNV when anti-VEGF is not feasible.

**Lifestyle & Monitoring**
- **Diet**: Increase intake of leafy greens (spinach, kale), oily fish (omega-3), and
  foods rich in lutein and zeaxanthin.
- **Supplements**: AREDS2 formulation (Vitamins C & E, Zinc, Copper, Lutein,
  Zeaxanthin) recommended for AMD patients.
- **Amsler Grid**: Daily home monitoring for distortion or new blind spots.
- **Follow-up**: OCT every 4–6 weeks during active treatment.

**Next Steps**
- Schedule retinal specialist appointment within **48–72 hours**.
- Begin anti-VEGF loading dose (3 monthly injections) as directed by your specialist.
"""

dme = """
**For DME (Diabetic Macular Edema)**

DME is a complication of diabetic retinopathy where fluid accumulates in the macula due
to leaking retinal blood vessels. It is the leading cause of vision loss in working-age
adults with diabetes.

---

**Immediate Action**
- Coordinate care between your **ophthalmologist** and **endocrinologist** — systemic
  diabetes control is equally important as local eye treatment.

**Treatment Options**
- **Anti-VEGF Injections** *(First-line)*: Ranibizumab, Aflibercept, or Bevacizumab
  reduce macular swelling and improve visual acuity. Monthly injections initially.
- **Intravitreal Corticosteroids**: Dexamethasone implant (Ozurdex) or triamcinolone
  for eyes unresponsive to anti-VEGF; higher risk of cataract and glaucoma.
- **Focal/Grid Laser Photocoagulation**: Treats microaneurysms and leaking vessels in
  non-centre-involving DME. Less used since anti-VEGF became standard.

**Systemic Control** *(Critical)*
- **HbA1c target**: Keep below **7%** — every 1% reduction lowers DME progression risk
  significantly.
- **Blood Pressure**: Target below **130/80 mmHg**; hypertension accelerates retinal
  vascular damage.
- **Lipids**: Statin therapy if dyslipidaemia is present.

**Monitoring**
- OCT scan every **3–6 months** to assess fluid levels and treatment response.
- Annual dilated fundus exam minimum.

**Next Steps**
- Schedule appointments with both retinal specialist and endocrinologist.
- Begin anti-VEGF treatment series and optimise systemic diabetes management.
"""

drusen = """
**For Drusen (Early Age-Related Macular Degeneration)**

Drusen are deposits of lipids and proteins that accumulate under the retinal pigment
epithelium. Their presence indicates early AMD and increases the risk of progression to
advanced wet or dry AMD with significant vision loss.

---

**Risk Stratification**
- **Small drusen** (< 63 µm): Low risk — routine monitoring.
- **Medium drusen** (63–124 µm): Moderate risk — lifestyle changes + supplements.
- **Large drusen** (≥ 125 µm) or geographic atrophy: High risk — close follow-up.

**Treatment & Prevention**
- **AREDS2 Supplements** *(Evidence-based)*: For intermediate or advanced AMD in one
  eye — Vitamin C 500mg, Vitamin E 400 IU, Zinc 80mg, Copper 2mg, Lutein 10mg,
  Zeaxanthin 2mg daily. Shown to reduce progression risk by ~25%.
- **No approved pharmacological treatment** for early drusen currently — prevention
  and monitoring are key.

**Lifestyle Modifications**
- **Quit Smoking**: Smoking doubles the risk of AMD progression — the single most
  important modifiable risk factor.
- **Diet**: Mediterranean-style diet rich in leafy greens, fish, nuts, and whole grains.
- **Exercise**: Regular physical activity associated with lower AMD progression rates.
- **UV Protection**: Quality sunglasses with UV400 protection outdoors.

**Monitoring**
- OCT every **6–12 months** to track drusen size, number, and pigment changes.
- **Amsler Grid** self-monitoring at home — report any new distortion immediately.

**Next Steps**
- Discuss AREDS2 supplementation with your ophthalmologist.
- Establish 6–12 monthly OCT review schedule.
"""

normal = """
**Normal Retina — No Pathology Detected**

Your OCT scan shows a healthy retina with a preserved foveal contour, no subretinal
fluid, no drusen deposits, and no signs of macular oedema or neovascularisation.

---

**Routine Eye Health Maintenance**
- **Annual Eye Exams**: Even with a normal scan, annual dilated fundus examination is
  recommended, especially if you have risk factors (family history of AMD, diabetes,
  hypertension, age > 50).
- **Self-Monitoring**: Use an Amsler grid weekly to detect any early changes in central
  vision that may warrant earlier review.

**Protective Measures**
- **Diet**: Maintain a diet rich in lutein and zeaxanthin (leafy greens), omega-3 fatty
  acids (oily fish), and antioxidant vitamins (C & E).
- **Sun Protection**: Wear UV-protective sunglasses when outdoors.
- **No Smoking**: Smoking is a major risk factor for future retinal disease.

**Systemic Health**
- Manage systemic conditions that can affect the retina — **diabetes**, **hypertension**,
  and **hyperlipidaemia** should be well-controlled.
- Blood glucose, blood pressure, and lipid checks annually if risk factors are present.

**Next Steps**
- No immediate treatment required.
- Schedule your next routine eye examination in **12 months**, or sooner if you notice
  any vision changes such as distortion, new floaters, or reduced central vision.
"""
