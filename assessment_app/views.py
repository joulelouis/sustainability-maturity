from django.shortcuts import render
import json

# Assessment structure based on IFRS S1 and S2 requirements.
assessment = {
    "Governance": [
        {
            "question": "To what extent does your organization have a formal structure for managing sustainability-related risks?",
            "options": {
                "1": "No formal structure exists; sustainability is addressed only at the executive level.",
                "2": "Initial awareness programs exist; limited cross-functional roles with minimal integration.",
                "3": "Formal oversight committees have been established with defined sustainability roles.",
                "4": "Robust framework with clear mandates and cross-functional integration.",
                "5": "Fully integrated, agile governance with continuous, real-time oversight across all levels."
            }
        }
        # Add additional Governance questions as needed.
    ],
    "Strategy": [
        {
            "question": "What types of data does your organization use to assess sustainability risks (climate, nature, and social)?",
            "options": {
                "1": "Generic offtheshelf data with no localization.",
                "2": "High-resolution localized data for select hazards.",
                "3": "Advanced data assessing individual and compounded hazards in pilot projects.",
                "4": "Comprehensive high-resolution data integrated into long-term planning.",
                "5": "Real-time, continuously updated data driving dynamic decision-making."
            }
        }
        # Add additional Strategy questions as needed.
    ],
    "Risk Management": [
        {
            "question": "How does your organization identify and assess sustainability risks (inherent vs. residual)?",
            "options": {
                "1": "Ad hoc identification using generic data focused on inherent risk only.",
                "2": "Basic assessments on select assets using localized data; inherent risk identified without residual analysis.",
                "3": "Pilot vulnerability assessments with advanced sensitivity analyses; initial residual risk evaluation using asset-specific parameters.",
                "4": "Systematic, full-scale assessments with rigorous stress testing and detailed residual risk evaluation.",
                "5": "Dynamic, continuous risk management with real-time monitoring and proactive management of both inherent and residual risks."
            }
        }
        # Add additional Risk Management questions as needed.
    ],
    "Performance Management": [
        {
            "question": "Do you have formal KPIs to measure sustainability performance and risk management outcomes?",
            "options": {
                "1": "No formal KPIs; reporting is limited to compliance-driven anecdotal evidence.",
                "2": "Initial qualitative and quantitative KPIs are introduced with limited scope.",
                "3": "Robust dashboards tracking pilot outcomes and early performance metrics are in place.",
                "4": "Sophisticated, data-driven KPIs are deployed organization-wide with structured reporting.",
                "5": "Benchmark-driven, real-time performance metrics with continuous improvement and automated reporting are in place."
            }
        }
        # Add additional Performance Management questions as needed.
    ]
}

# Recommendations for each pillar and maturity level.
recommendations = {
    "Governance": {
        "1": "Establish basic awareness sessions and introductory training for top management; define initial roles.",
        "2": "Develop structured training programs and designate sustainability champions across key functions.",
        "3": "Establish formal oversight committees and assign clear, cross-functional roles.",
        "4": "Implement a robust governance framework with integrated, organization-wide reporting.",
        "5": "Embed agile, real-time governance processes with continuous, organization-wide participation."
    },
    "Strategy": {
        "1": "Utilize generic data tools and begin basic analysis for compliance reporting.",
        "2": "Invest in localized data acquisition and initiate basic sensitivity analyses.",
        "3": "Deploy advanced loss models and pilot projects to aggregate asset-level data; begin residual risk estimation.",
        "4": "Integrate full-scale vulnerability assessments and develop comprehensive, climate-adjusted financial projections.",
        "5": "Implement real-time analytics and dynamic strategic planning processes across the entire value chain."
    },
    "Risk Management": {
        "1": "Begin ad hoc risk identification using generic data; document basic processes.",
        "2": "Conduct basic assessments on critical assets and introduce simple sensitivity testing.",
        "3": "Implement pilot vulnerability assessments with initial residual risk evaluations.",
        "4": "Adopt systematic, full-scale assessments with rigorous stress testing and detailed residual risk analysis.",
        "5": "Deploy advanced digital tools for continuous, proactive risk management with real-time monitoring."
    },
    "Performance Management": {
        "1": "Set up minimal documentation for compliance reporting; no formal KPIs yet.",
        "2": "Introduce preliminary KPIs and basic internal reviews.",
        "3": "Develop robust dashboards that track pilot outcomes and quantify early performance.",
        "4": "Establish sophisticated, data-driven KPIs and structured reporting frameworks.",
        "5": "Implement fully integrated, real-time performance monitoring systems with continuous improvement loops."
    }
}

# Generate summary insights (strengths and gaps) for each pillar.
def generate_summary(pillar_scores):
    summaries = {}
    for pillar, score in pillar_scores.items():
        if score <= 2:
            summaries[pillar] = (
                f"Your {pillar} approach is at an early stage. Key gaps include the lack of formal structures, "
                f"limited integration, and minimal cross-functional involvement. Focus on establishing foundational "
                f"systems and training."
            )
        elif score == 3:
            summaries[pillar] = (
                f"Your {pillar} practices are emerging with formal processes in place. There's an opportunity to "
                f"integrate advanced analytics and increase cross-functional collaboration for further refinement."
            )
        elif score == 4:
            summaries[pillar] = (
                f"Your {pillar} processes are well established and optimized, with strong integration and advanced "
                f"methodologies. Minor improvements can drive incremental benefits."
            )
        else:
            summaries[pillar] = (
                f"Your {pillar} maturity is highly advanced, with agile, real-time systems. Continue focusing on "
                f"continuous improvement and innovative practices."
            )
    return summaries

def index(request):
    # Render the form with the assessment data.
    context = {'assessment': assessment}
    return render(request, 'index.html', context)

def results(request):
    if request.method == 'POST':
        pillar_scores = {}
        pillar_recommendations = {}
        for pillar in assessment:
            total = 0
            count = 0
            for idx, question in enumerate(assessment[pillar]):
                key = f"{pillar}_{idx}"
                answer = request.POST.get(key)
                if answer and answer.isdigit():
                    total += int(answer)
                    count += 1
            avg_score = round(total / count) if count > 0 else 0
            pillar_scores[pillar] = avg_score
            pillar_recommendations[pillar] = recommendations[pillar].get(str(avg_score), "No recommendation available.")
    
        overall_maturity = round(sum(pillar_scores.values()) / len(pillar_scores))
        summary_text = generate_summary(pillar_scores)
    
        # Convert scores to JSON for use in visualizations if needed (e.g., Chart.js).
        scores_json = json.dumps(pillar_scores)
    
        context = {
            'pillar_scores': pillar_scores,
            'overall_maturity': overall_maturity,
            'pillar_recommendations': pillar_recommendations,
            'summary_text': summary_text,
            'scores_json': scores_json,
        }
        return render(request, 'results.html', context)
    else:
        # If accessed via GET, redirect back to the index page.
        context = {'assessment': assessment}
        return render(request, 'index.html', context)

