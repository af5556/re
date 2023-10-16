--on bdd sol_widget--
SELECT
    r.leadId AS id,
    r.test AS test,
    cd.reg_number AS regNumber,
    DATE(rm.timestamp) AS timestamp,
    COUNT(cda.id) As carDamage,
    r.widget_id As widgetId,
    DATE(bc.availability_date) AS availabilityDate,
    DATE(va.valuation_date) As valuationDate,
    DATE(va.estimate_valuation_date) As estimateValuationDate,
    r.brand_mop As brandMop,
    r.type_mop As typeMop,
    DATE(r.creation_at) As creationAt,
    TIME(r.creation_at) As creationHour,
    r.chrono_id AS chronoId,
    r.mop_id AS mopId,
    r.brand As brand,
    r.country As country,
    r.status As status,
    rs.label As label,
    r.last_step_visited As lastStepVisited,
    va.estimate_accepted AS estimateAccepted,
    va.accepted AS accepted,
    cd.make_name AS makeName,
    cd.model_name AS modelName,
    cd.fuel_type_name AS fuelTypeName,
    cd.version_name As versionName,
    cd.first_registration AS firstRegistration,
    cs.overall_mileage As overallMileage,
    cs.annual_mileage As annualMileage,
    cs.expected_mileage As expectedMileage,
    r.excluded As excluded,
    cs.owned_car As registrationCertificateName,
    cs.pawned_car As pledged,
    cs.rolling_car As roll,
    cs.accidented_car As state,
    cs.imported_car As import,
    cs.technical_control As technicalControl,
    cs.front_tires_condition As frontTiresCondition,
    cs.rear_tires_condition As rearTiresCondition,
    cs.mechanical_condition As mechanicalCondition,
    cs.electronic_condition As electronicCondition,
    cs.service_history As serviceHistory,
    cs.interior_condition As interiorCondition,
    fb.answer As answer,
    va.estimate_valuation_applied As estimateValuationApplied,
    va.estimated_frevo_stat As estimatedFrevoStat,
    va.frevo_stat As frevoStat,
    va.frevo_damage As frevoDamage,
    va.quotation As quotation,
    va.valuation_applied As valuationApplied,
    bc.amount As amount,
    r.commercial As commercial,
    bc.price_vn As priceVn,
    d.name As name,
    d.address As address,
    d.zipCode As zipCode,
    d.phone As phone,
    r.user_action As userAction,
    r.last_step_visited as lastStepVisited,
    d.rrdiCode As rrdiCode,
    r.duplicate_ind As duplicateInd,
    va.median_ind As medianInd,
    r.valuation_key As valuationKey,
    w.api_key as apiKey,
    w.label as widgetName,
    r.updated_at as updatedAt
FROM
    record AS r
    LEFT JOIN car_details AS cd on r.car_details_id = cd.id
    LEFT JOIN car_damage AS cda on r.leadid = cda.record_id
    LEFT JOIN record_media AS rm on r.leadId = rm.record_id
    LEFT JOIN widget AS w on r.widget_id = w.id
    LEFT JOIN valuation AS va on r.valuation_id = va.id
    LEFT JOIN brand_contribution AS bc on va.brand_contribution_id = bc.id
    LEFT JOIN record_status AS rs on r.status = rs.id
    LEFT JOIN car_state AS cs on cd.car_state_id = cs.id
    LEFT JOIN feedback_answer AS fb on r.feedback_answer_id = fb.id
    LEFT JOIN personal_details AS pd on r.personal_details_id = pd.id
    LEFT JOIN dealer As d on pd.dealer_id = d.id
WHERE
    r.creation_at BETWEEN {yesterday} AND {today} OR r.updated_at BETWEEN {yesterday} AND {today}
GROUP BY id,timestamp