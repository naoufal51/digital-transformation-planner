from typing import Dict, List

def get_standard_categories() -> List[Dict]:
    """Get standard technology categories for digital transformation"""
    return [
        {
            "name": "Customer Experience Platforms",
            "description": "Solutions that improve customer interactions and engagement across channels",
            "related_dimension": "Customer Experience",
            "supports_goals": [
                "Improve customer experience", 
                "Increase customer retention",
                "Enhance digital channels"
            ],
            "addresses_challenges": [
                "Poor customer engagement",
                "Limited digital presence",
                "Siloed customer data",
                "High customer churn"
            ],
            "sample_technologies": [
                {
                    "name": "Salesforce Experience Cloud",
                    "vendor": "Salesforce",
                    "description": "Cloud-based platform for creating digital experiences for customers, partners, and employees",
                    "key_features": [
                        "Unified customer profiles", 
                        "Personalization engine", 
                        "Multichannel engagement", 
                        "Self-service portals"
                    ],
                    "pros": [
                        "Robust ecosystem and integrations", 
                        "Comprehensive analytics", 
                        "No-code/low-code capabilities"
                    ],
                    "cons": [
                        "High cost", 
                        "Complex implementation", 
                        "May require specialized development"
                    ],
                    "cost_range": "$$$",
                    "implementation_complexity": "High",
                    "industry_focus": ["All"],
                    "integrations": ["Salesforce CRM", "Marketing automation", "ERP systems"],
                    "supports_goals": ["Improve customer experience", "Increase sales"],
                    "addresses_challenges": ["Siloed customer data", "Poor customer engagement"]
                },
                {
                    "name": "Adobe Experience Cloud",
                    "vendor": "Adobe",
                    "description": "Integrated suite of solutions for marketing, analytics, and content management",
                    "key_features": [
                        "Content management", 
                        "Marketing automation", 
                        "Personalization", 
                        "Customer analytics"
                    ],
                    "pros": [
                        "Comprehensive suite", 
                        "Strong analytics capabilities", 
                        "Excellent content tools"
                    ],
                    "cons": [
                        "Expensive", 
                        "Requires technical expertise", 
                        "Complex architecture"
                    ],
                    "cost_range": "$$$",
                    "implementation_complexity": "High",
                    "industry_focus": ["Retail", "Financial Services", "Healthcare"],
                    "integrations": ["CRM systems", "ERP", "E-commerce platforms"],
                    "supports_goals": ["Digital marketing transformation", "Content personalization"],
                    "addresses_challenges": ["Inconsistent brand experience", "Limited digital presence"]
                },
                {
                    "name": "HubSpot CRM Suite",
                    "vendor": "HubSpot",
                    "description": "All-in-one CRM platform with marketing, sales, and service hubs",
                    "key_features": [
                        "Contact management", 
                        "Email marketing", 
                        "Live chat", 
                        "Customer service tools"
                    ],
                    "pros": [
                        "User-friendly interface", 
                        "Affordable entry point", 
                        "Quick implementation"
                    ],
                    "cons": [
                        "Limited customization", 
                        "Less robust for enterprise needs", 
                        "Can become expensive at scale"
                    ],
                    "cost_range": "$$",
                    "implementation_complexity": "Low",
                    "industry_focus": ["SMBs", "B2B", "Professional Services"],
                    "integrations": ["Gmail", "Outlook", "Shopify", "WordPress"],
                    "supports_goals": ["Sales and marketing alignment", "Lead generation"],
                    "addresses_challenges": ["Disjointed customer journey", "Manual sales processes"]
                }
            ]
        },
        {
            "name": "Data Management & Analytics",
            "description": "Solutions for collecting, storing, analyzing, and deriving insights from data",
            "related_dimension": "Data & Analytics",
            "supports_goals": [
                "Data-driven decision making", 
                "Improve operational efficiency",
                "Enhance business intelligence"
            ],
            "addresses_challenges": [
                "Poor data quality",
                "Siloed data systems",
                "Limited analytics capabilities",
                "Difficulty accessing insights"
            ],
            "sample_technologies": [
                {
                    "name": "Snowflake Data Cloud",
                    "vendor": "Snowflake",
                    "description": "Cloud-based data platform for storage, processing, and analytics workloads",
                    "key_features": [
                        "Multi-cloud support", 
                        "Separation of storage and compute", 
                        "Data sharing", 
                        "Scalable performance"
                    ],
                    "pros": [
                        "Excellent performance", 
                        "Flexible scaling", 
                        "Pay-per-use model"
                    ],
                    "cons": [
                        "Can be expensive for large workloads", 
                        "Requires SQL knowledge", 
                        "Complex pricing model"
                    ],
                    "cost_range": "$$$",
                    "implementation_complexity": "Medium",
                    "industry_focus": ["All"],
                    "integrations": ["BI tools", "ETL/ELT tools", "ML platforms"],
                    "supports_goals": ["Data consolidation", "Analytics modernization"],
                    "addresses_challenges": ["Siloed data", "Scalability limitations"]
                },
                {
                    "name": "Tableau",
                    "vendor": "Salesforce",
                    "description": "Visual analytics platform for business intelligence and data visualization",
                    "key_features": [
                        "Interactive dashboards", 
                        "Data blending", 
                        "Natural language queries", 
                        "Mobile analytics"
                    ],
                    "pros": [
                        "Intuitive interface", 
                        "Powerful visualizations", 
                        "Strong community support"
                    ],
                    "cons": [
                        "Expensive per-user licensing", 
                        "Performance issues with large datasets", 
                        "Limited data wrangling capabilities"
                    ],
                    "cost_range": "$$",
                    "implementation_complexity": "Medium",
                    "industry_focus": ["All"],
                    "integrations": ["Multiple data sources", "CRM systems", "Cloud platforms"],
                    "supports_goals": ["Better business insights", "Data democratization"],
                    "addresses_challenges": ["Limited data visibility", "Slow reporting processes"]
                },
                {
                    "name": "Microsoft Power BI",
                    "vendor": "Microsoft",
                    "description": "Business analytics service for interactive visualizations and business intelligence",
                    "key_features": [
                        "Self-service analytics", 
                        "AI capabilities", 
                        "Office 365 integration", 
                        "Embedded analytics"
                    ],
                    "pros": [
                        "Cost-effective", 
                        "Good Microsoft ecosystem integration", 
                        "User-friendly"
                    ],
                    "cons": [
                        "Some limitations with complex visualizations", 
                        "Not as powerful for very large datasets", 
                        "Best with Microsoft stack"
                    ],
                    "cost_range": "$",
                    "implementation_complexity": "Low",
                    "industry_focus": ["All"],
                    "integrations": ["Microsoft 365", "Azure", "Dynamics 365"],
                    "supports_goals": ["Self-service analytics", "Operational reporting"],
                    "addresses_challenges": ["Spreadsheet overload", "Inconsistent reporting"]
                }
            ]
        },
        {
            "name": "Core Systems Modernization",
            "description": "Solutions to update or replace legacy core business systems with modern technologies",
            "related_dimension": "Enterprise Technology",
            "supports_goals": [
                "Increase operational efficiency", 
                "Improve system flexibility",
                "Reduce technical debt"
            ],
            "addresses_challenges": [
                "Legacy system constraints",
                "High maintenance costs",
                "Integration difficulties",
                "Poor performance"
            ],
            "sample_technologies": [
                {
                    "name": "SAP S/4HANA",
                    "vendor": "SAP",
                    "description": "Intelligent ERP system for digital business processes",
                    "key_features": [
                        "In-memory database", 
                        "Real-time analytics", 
                        "AI/ML capabilities", 
                        "Simplified data model"
                    ],
                    "pros": [
                        "Comprehensive functionality", 
                        "Industry-specific solutions", 
                        "Strong ecosystem"
                    ],
                    "cons": [
                        "High cost", 
                        "Complex implementation", 
                        "Significant change management required"
                    ],
                    "cost_range": "$$$",
                    "implementation_complexity": "High",
                    "industry_focus": ["Manufacturing", "Retail", "Financial Services"],
                    "integrations": ["CRM", "Supply chain", "HR systems"],
                    "supports_goals": ["Process standardization", "Digital core transformation"],
                    "addresses_challenges": ["Legacy ERP limitations", "Data inconsistency"]
                },
                {
                    "name": "Microsoft Dynamics 365",
                    "vendor": "Microsoft",
                    "description": "Cloud-based business applications suite combining ERP and CRM capabilities",
                    "key_features": [
                        "Modular applications", 
                        "AI insights", 
                        "Office 365 integration", 
                        "Mixed reality capabilities"
                    ],
                    "pros": [
                        "Familiar Microsoft interface", 
                        "Flexible deployment options", 
                        "Good value for features"
                    ],
                    "cons": [
                        "Implementation complexity", 
                        "Customization can be challenging", 
                        "Some modules less mature than competitors"
                    ],
                    "cost_range": "$$",
                    "implementation_complexity": "Medium",
                    "industry_focus": ["Professional Services", "Retail", "Manufacturing"],
                    "integrations": ["Office 365", "Power Platform", "Azure services"],
                    "supports_goals": ["Business application consolidation", "Cloud migration"],
                    "addresses_challenges": ["Disconnected business systems", "Manual processes"]
                },
                {
                    "name": "Oracle NetSuite",
                    "vendor": "Oracle",
                    "description": "Cloud-based business management suite including ERP, CRM, and e-commerce",
                    "key_features": [
                        "Unified business data", 
                        "Role-based dashboards", 
                        "Automated processes", 
                        "Global business management"
                    ],
                    "pros": [
                        "Fast implementation", 
                        "Regular automatic updates", 
                        "Good for growing businesses"
                    ],
                    "cons": [
                        "Less customizable than some alternatives", 
                        "Can be expensive at scale", 
                        "Limited industry-specific functionality"
                    ],
                    "cost_range": "$$",
                    "implementation_complexity": "Medium",
                    "industry_focus": ["Professional Services", "Wholesale Distribution", "Software"],
                    "integrations": ["E-commerce platforms", "Payment processors", "CRM systems"],
                    "supports_goals": ["Unified business platform", "Process automation"],
                    "addresses_challenges": ["Business visibility", "Growth limitations"]
                }
            ]
        },
        {
            "name": "Advanced AI & Automation",
            "description": "Solutions leveraging artificial intelligence, machine learning, and automation to transform business processes",
            "related_dimension": "Intelligent Automation",
            "supports_goals": [
                "Automate manual processes", 
                "Enhance decision making",
                "Create new business capabilities"
            ],
            "addresses_challenges": [
                "Operational inefficiency",
                "Labor-intensive processes",
                "Inconsistent quality",
                "Slow response times"
            ],
            "sample_technologies": [
                {
                    "name": "UiPath",
                    "vendor": "UiPath",
                    "description": "Robotic Process Automation (RPA) platform for automating repetitive tasks",
                    "key_features": [
                        "Process mining", 
                        "Attended and unattended automation", 
                        "AI capabilities", 
                        "Low-code development"
                    ],
                    "pros": [
                        "User-friendly design studio", 
                        "Strong community support", 
                        "Comprehensive ecosystem"
                    ],
                    "cons": [
                        "Can be expensive for enterprise deployment", 
                        "Requires governance framework", 
                        "Maintenance overhead"
                    ],
                    "cost_range": "$$",
                    "implementation_complexity": "Medium",
                    "industry_focus": ["Financial Services", "Healthcare", "Insurance"],
                    "integrations": ["ERP systems", "CRM systems", "Legacy applications"],
                    "supports_goals": ["Process automation", "Cost reduction"],
                    "addresses_challenges": ["Manual processes", "Data entry errors"]
                },
                {
                    "name": "DataRobot",
                    "vendor": "DataRobot",
                    "description": "Enterprise AI platform for building and deploying machine learning models",
                    "key_features": [
                        "Automated machine learning", 
                        "Model deployment", 
                        "Model monitoring", 
                        "AI services"
                    ],
                    "pros": [
                        "Accessible to non-data scientists", 
                        "Rapid model development", 
                        "End-to-end ML lifecycle"
                    ],
                    "cons": [
                        "High cost", 
                        "Black box approach reduces transparency", 
                        "May still require data science expertise"
                    ],
                    "cost_range": "$$$",
                    "implementation_complexity": "High",
                    "industry_focus": ["Financial Services", "Healthcare", "Retail"],
                    "integrations": ["Data platforms", "BI tools", "Business applications"],
                    "supports_goals": ["AI adoption", "Predictive analytics"],
                    "addresses_challenges": ["Underutilized data", "Reactive decision making"]
                },
                {
                    "name": "Microsoft Power Automate",
                    "vendor": "Microsoft",
                    "description": "Cloud-based service for automating workflows across applications and services",
                    "key_features": [
                        "Process automation", 
                        "Desktop automation", 
                        "AI Builder", 
                        "Pre-built connectors"
                    ],
                    "pros": [
                        "Cost-effective", 
                        "Easy to learn", 
                        "Strong Microsoft integration"
                    ],
                    "cons": [
                        "Limited capabilities for complex processes", 
                        "Performance can be inconsistent", 
                        "Best within Microsoft ecosystem"
                    ],
                    "cost_range": "$",
                    "implementation_complexity": "Low",
                    "industry_focus": ["All"],
                    "integrations": ["Microsoft 365", "Dynamics 365", "Third-party services"],
                    "supports_goals": ["Workflow automation", "Citizen development"],
                    "addresses_challenges": ["Process inefficiencies", "Manual task overhead"]
                }
            ]
        },
        {
            "name": "Cloud Infrastructure & DevOps",
            "description": "Solutions for modern cloud infrastructure, development practices, and operational models",
            "related_dimension": "Enterprise Technology",
            "supports_goals": [
                "Increase agility", 
                "Improve scalability",
                "Reduce infrastructure costs"
            ],
            "addresses_challenges": [
                "On-premises infrastructure limitations",
                "Slow deployment cycles",
                "High operational costs",
                "Limited scaling capabilities"
            ],
            "sample_technologies": [
                {
                    "name": "AWS Cloud",
                    "vendor": "Amazon",
                    "description": "Comprehensive cloud platform with hundreds of services for computing, storage, and more",
                    "key_features": [
                        "Elastic compute", 
                        "Global infrastructure", 
                        "Pay-as-you-go pricing", 
                        "Advanced security"
                    ],
                    "pros": [
                        "Most mature cloud provider", 
                        "Extensive service catalog", 
                        "Strong ecosystem"
                    ],
                    "cons": [
                        "Complex pricing", 
                        "Management overhead", 
                        "Can require specialized expertise"
                    ],
                    "cost_range": "$$",
                    "implementation_complexity": "Medium",
                    "industry_focus": ["All"],
                    "integrations": ["Most enterprise systems", "Third-party tools"],
                    "supports_goals": ["Cloud migration", "Infrastructure modernization"],
                    "addresses_challenges": ["Scalability limits", "High infrastructure costs"]
                },
                {
                    "name": "Microsoft Azure",
                    "vendor": "Microsoft",
                    "description": "Cloud computing platform for building, testing, deploying, and managing applications",
                    "key_features": [
                        "Hybrid cloud capabilities", 
                        "Strong enterprise integration", 
                        "Advanced analytics", 
                        "AI services"
                    ],
                    "pros": [
                        "Good for Microsoft-centric organizations", 
                        "Strong identity management", 
                        "Enterprise agreements leverage"
                    ],
                    "cons": [
                        "Some services less mature than AWS", 
                        "Can be complex to optimize costs", 
                        "Documentation gaps"
                    ],
                    "cost_range": "$$",
                    "implementation_complexity": "Medium",
                    "industry_focus": ["All"],
                    "integrations": ["Microsoft 365", "Windows environments", "Enterprise systems"],
                    "supports_goals": ["Hybrid cloud strategy", "Digital workspace"],
                    "addresses_challenges": ["Legacy infrastructure", "Integration complexity"]
                },
                {
                    "name": "GitLab DevOps Platform",
                    "vendor": "GitLab",
                    "description": "Complete DevOps platform for software development, security, and operations",
                    "key_features": [
                        "Source code management", 
                        "CI/CD pipelines", 
                        "Security scanning", 
                        "Project management"
                    ],
                    "pros": [
                        "All-in-one platform", 
                        "Strong collaboration features", 
                        "Regular updates"
                    ],
                    "cons": [
                        "Can be resource intensive", 
                        "Learning curve for full platform", 
                        "Some features less polished than point solutions"
                    ],
                    "cost_range": "$$",
                    "implementation_complexity": "Medium",
                    "industry_focus": ["Technology", "Financial Services", "Healthcare"],
                    "integrations": ["Cloud platforms", "Monitoring tools", "Issue trackers"],
                    "supports_goals": ["DevOps transformation", "Development acceleration"],
                    "addresses_challenges": ["Slow release cycles", "Development silos"]
                }
            ]
        }
    ]


def get_industry_specific_categories(industry: str) -> List[Dict]:
    """Get industry-specific technology categories for digital transformation"""
    
    industry_categories = {
        "Healthcare": [
            {
                "name": "Telehealth Platforms",
                "description": "Solutions enabling remote healthcare delivery and virtual patient engagement",
                "related_dimension": "Customer Experience",
                "supports_goals": [
                    "Improve patient access", 
                    "Expand service delivery",
                    "Reduce costs"
                ],
                "addresses_challenges": [
                    "Limited access to care",
                    "High no-show rates",
                    "Provider capacity constraints",
                    "Geographic limitations"
                ],
                "sample_technologies": [
                    {
                        "name": "Teladoc Health",
                        "vendor": "Teladoc Health",
                        "description": "Virtual care delivery platform for telehealth visits and remote monitoring",
                        "key_features": [
                            "Video visits", 
                            "Remote monitoring", 
                            "EHR integration", 
                            "Multi-specialty support"
                        ],
                        "pros": [
                            "Comprehensive platform", 
                            "Strong clinical protocols", 
                            "Extensive provider network"
                        ],
                        "cons": [
                            "High implementation cost", 
                            "Complex integration", 
                            "Subscription model can be expensive"
                        ],
                        "cost_range": "$$$",
                        "implementation_complexity": "High",
                        "industry_focus": ["Healthcare"],
                        "integrations": ["EHR systems", "Patient portals", "Practice management"],
                        "supports_goals": ["Virtual care expansion", "Patient access"],
                        "addresses_challenges": ["Geographic limitations", "Provider shortage"]
                    },
                    {
                        "name": "Zoom for Healthcare",
                        "vendor": "Zoom",
                        "description": "HIPAA-compliant video communication platform for healthcare providers",
                        "key_features": [
                            "Secure video visits", 
                            "Waiting room", 
                            "Screen sharing", 
                            "Team collaboration"
                        ],
                        "pros": [
                            "Familiar interface", 
                            "Easy to implement", 
                            "Cost-effective"
                        ],
                        "cons": [
                            "Limited healthcare-specific features", 
                            "Basic EHR integrations", 
                            "Not a complete telehealth solution"
                        ],
                        "cost_range": "$",
                        "implementation_complexity": "Low",
                        "industry_focus": ["Healthcare", "Education"],
                        "integrations": ["EHR systems", "Scheduling tools"],
                        "supports_goals": ["Quick telehealth implementation", "Staff collaboration"],
                        "addresses_challenges": ["Urgent virtual care needs", "Remote consultation"]
                    }
                ]
            },
            {
                "name": "Healthcare Analytics",
                "description": "Solutions for analyzing clinical, operational, and financial healthcare data",
                "related_dimension": "Data & Analytics",
                "supports_goals": [
                    "Improve clinical outcomes", 
                    "Optimize operations",
                    "Reduce costs"
                ],
                "addresses_challenges": [
                    "Care variation",
                    "Utilization management",
                    "Population health",
                    "Revenue cycle optimization"
                ],
                "sample_technologies": [
                    {
                        "name": "Health Catalyst",
                        "vendor": "Health Catalyst",
                        "description": "Data platform and analytics solution designed specifically for healthcare",
                        "key_features": [
                            "Clinical data repository", 
                            "Population health", 
                            "Financial analytics", 
                            "Quality improvement"
                        ],
                        "pros": [
                            "Healthcare-specific data models", 
                            "Clinical expertise", 
                            "Implementation support"
                        ],
                        "cons": [
                            "High cost", 
                            "Complex implementation", 
                            "Requires dedicated analysts"
                        ],
                        "cost_range": "$$$",
                        "implementation_complexity": "High",
                        "industry_focus": ["Healthcare"],
                        "integrations": ["EHR systems", "Claims data", "Financial systems"],
                        "supports_goals": ["Clinical improvement", "Cost reduction"],
                        "addresses_challenges": ["Data silos", "Performance variation"]
                    }
                ]
            }
        ],
        "Manufacturing": [
            {
                "name": "Industrial IoT Platforms",
                "description": "Solutions for connecting, monitoring, and optimizing manufacturing equipment and processes",
                "related_dimension": "Enterprise Technology",
                "supports_goals": [
                    "Improve operational efficiency", 
                    "Reduce downtime",
                    "Enable predictive maintenance"
                ],
                "addresses_challenges": [
                    "Equipment failures",
                    "Production inefficiencies",
                    "Quality issues",
                    "Limited visibility"
                ],
                "sample_technologies": [
                    {
                        "name": "PTC ThingWorx",
                        "vendor": "PTC",
                        "description": "Industrial IoT platform for connecting machines and enabling smart manufacturing",
                        "key_features": [
                            "Device connectivity", 
                            "Real-time monitoring", 
                            "AR experiences", 
                            "Predictive analytics"
                        ],
                        "pros": [
                            "Comprehensive platform", 
                            "Strong AR capabilities", 
                            "Industry expertise"
                        ],
                        "cons": [
                            "Expensive", 
                            "Complex implementation", 
                            "May require specialized development"
                        ],
                        "cost_range": "$$$",
                        "implementation_complexity": "High",
                        "industry_focus": ["Manufacturing", "Industrial"],
                        "integrations": ["ERP systems", "MES", "SCADA systems"],
                        "supports_goals": ["Smart factory", "Equipment optimization"],
                        "addresses_challenges": ["Equipment downtime", "Visibility gaps"]
                    }
                ]
            }
        ],
        "Retail": [
            {
                "name": "Omnichannel Commerce",
                "description": "Solutions for unified commerce across physical and digital channels",
                "related_dimension": "Customer Experience",
                "supports_goals": [
                    "Increase sales", 
                    "Improve customer experience",
                    "Enable new business models"
                ],
                "addresses_challenges": [
                    "Channel fragmentation",
                    "Inventory visibility",
                    "Customer expectations",
                    "Digital competition"
                ],
                "sample_technologies": [
                    {
                        "name": "Shopify Plus",
                        "vendor": "Shopify",
                        "description": "Enterprise e-commerce platform for omnichannel retail",
                        "key_features": [
                            "Multi-channel selling", 
                            "Inventory management", 
                            "Customization", 
                            "Fulfillment integration"
                        ],
                        "pros": [
                            "Quick implementation", 
                            "User-friendly", 
                            "Strong ecosystem"
                        ],
                        "cons": [
                            "Limited B2B capabilities", 
                            "Can be expensive at scale", 
                            "Some customization limitations"
                        ],
                        "cost_range": "$$",
                        "implementation_complexity": "Medium",
                        "industry_focus": ["Retail", "Direct-to-Consumer"],
                        "integrations": ["ERP", "Marketplaces", "POS systems"],
                        "supports_goals": ["Digital commerce expansion", "Unified experience"],
                        "addresses_challenges": ["Limited online presence", "Channel silos"]
                    }
                ]
            }
        ],
        "Financial Services": [
            {
                "name": "Digital Banking Platforms",
                "description": "Solutions for delivering modern digital banking experiences and services",
                "related_dimension": "Customer Experience",
                "supports_goals": [
                    "Improve customer experience", 
                    "Increase digital engagement",
                    "Reduce operational costs"
                ],
                "addresses_challenges": [
                    "Legacy systems",
                    "Customer expectations",
                    "Fintech competition",
                    "Cost pressures"
                ],
                "sample_technologies": [
                    {
                        "name": "Temenos Infinity",
                        "vendor": "Temenos",
                        "description": "Digital banking platform for customer experience and engagement",
                        "key_features": [
                            "Omnichannel banking", 
                            "Customer onboarding", 
                            "Personal financial management", 
                            "Marketing capabilities"
                        ],
                        "pros": [
                            "Comprehensive platform", 
                            "Financial services expertise", 
                            "Modular approach"
                        ],
                        "cons": [
                            "Expensive", 
                            "Complex implementation", 
                            "Requires significant IT resources"
                        ],
                        "cost_range": "$$$",
                        "implementation_complexity": "High",
                        "industry_focus": ["Banking", "Financial Services"],
                        "integrations": ["Core banking", "Payment systems", "CRM"],
                        "supports_goals": ["Digital transformation", "Customer acquisition"],
                        "addresses_challenges": ["Legacy customer experience", "Digital competition"]
                    }
                ]
            }
        ],
        "Education": [
            {
                "name": "Learning Management Systems",
                "description": "Platforms for delivering, managing, and tracking educational content and experiences",
                "related_dimension": "Customer Experience",
                "supports_goals": [
                    "Improve student engagement", 
                    "Expand educational access",
                    "Enhance learning outcomes"
                ],
                "addresses_challenges": [
                    "Remote learning needs",
                    "Student engagement",
                    "Content management",
                    "Learning assessment"
                ],
                "sample_technologies": [
                    {
                        "name": "Canvas LMS",
                        "vendor": "Instructure",
                        "description": "Cloud-based learning management system for educational institutions",
                        "key_features": [
                            "Course management", 
                            "Assessment tools", 
                            "Mobile access", 
                            "Analytics"
                        ],
                        "pros": [
                            "User-friendly interface", 
                            "Strong mobile experience", 
                            "Regular updates"
                        ],
                        "cons": [
                            "Can be expensive for small institutions", 
                            "Some advanced features require add-ons", 
                            "Limited customization"
                        ],
                        "cost_range": "$$",
                        "implementation_complexity": "Medium",
                        "industry_focus": ["Higher Education", "K-12"],
                        "integrations": ["SIS systems", "Video platforms", "Content repositories"],
                        "supports_goals": ["Digital learning transformation", "Remote education"],
                        "addresses_challenges": ["Engagement", "Course management complexity"]
                    }
                ]
            }
        ]
    }
    
    # Return the categories for the specified industry, or an empty list if not found
    return industry_categories.get(industry, []) 