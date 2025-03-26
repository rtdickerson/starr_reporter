# starr_reporter
Ingest STARR test reports from TEA and make reports.

The STARR reports 3 outcomes:

Approaches Grade Level: Performance in this category indicates that students are likely to succeed in the next grade or course with targeted academic intervention. Students in this category generally demonstrate the ability to apply the assessed knowledge and skills in familiar contexts.

Meets Grade Level:  Performance in this category indicates that students have a high likelihood of success in the next grade or course but may still need some short-term, targeted academic intervention. Students in this category generally demonstrate the ability to think critically and apply the assessed knowledge and skills in familiar contexts.

Masters Grade Level : Performance in this category indicates that students are expected to succeed in the next grade or course with little or no academic intervention. Students in this category demonstrate the ability to think critically and apply the assessed knowledge and skills in varied contexts, both familiar and unfamiliar.

There's a 4th result they don't put in the report..

Did Not Meet Grade Level:  Performance in this category indicates that students are unlikely to succeed in the next grade or course without significant, ongoing academic intervention. Students in this category do not demonstrate a sufficient understanding of the assessed knowledge and skills.

The first 3 groups overlap.  So the "approaches" includes the "met" and "masters".  The "met" includes the "masters"  But the 4th group isn't mentioned.

If we liken the STARR test results to an aircraft carrier.. the "met" guys stuck the landing, but the "master" guys caught the first wire!  The "approaches" pilots put their plane in the drink and SAR had to rescue them and take them to the carrier.  This 4th group is so lost even SAR couldn't find them.  They're the lost generation.

This tool will parse their data and re-organizes it so you can actually see trends and performance data.  The output is a CSV file that you can import into Excel.

Source: https://tea.texas.gov/student-assessment/student-assessment-results/statewide-summary-reports
https://rptsvr1.tea.texas.gov/cgi/sas/broker?_service=marykay&_program=perfrept.perfmast.sas&_debug=0&ccyy=2024&lev=D&id=247901&prgopt=reports/tapr/fed_performance.sas



