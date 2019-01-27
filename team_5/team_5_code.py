import os
print("Entity name")
os.system("pdfgrep ' Ltd ' *.pdf")
os.system("pdfgrep ' INC.' *.pdf")
os.system("pdfgrep ' PLC ' *.pdf")

print("\n")
print("\n")

print("Audit Peroid")
os.system("pdfgrep -A2 -B2 'present their statement to the members' *.pdf")
os.system("pdfgrep -A2 -B2 'audited financial statements' *.pdf")

print("\n")
print("\n")

print("auditor opinion")
os.system("pdfgrep -A6 -B1 'the accompanying consolidated financial statements of' *.pdf")
os.system("pdfgrep -A6 -B1 'We have audited the consolidated financial statements' *.pdf")
os.system("pdfgrep -A6 -B1 'In the opinion of' *.pdf")
os.system("pdfgrep -A6 -B1 'report that includes our opinion' *.pdf")
os.system("pdfgrep -A6 -B1 'In our opinion, the accompanying consolidated financial statements of' *.pdf")
os.system("pdfgrep -A6 -B1 'In our opinion, the accompanying consolidated financial statements of the Group' *.pdf")
print("\n")
print("\n")


print("name of auditor")
os.system("pdfgrep -A2 -B2 'Chartered Accountants' *.pdf")
os.system("pdfgrep -A2 -B2 'the external auditor' *.pdf")
os.system("pdfgrep -A2 -B2 'Public Accountants' *.pdf")
print("\n")
print("\n")

print("Revenue")
os.system("pdfgrep 'Total revenue' *.pdf")
os.system("pdfgrep 'Revenue' *.pdf")
print("\n")
print("\n")


print("Net profit")
os.system("pdfgrep 'Profit after tax' *.pdf")
os.system("pdfgrep 'Profit for the year' *.pdf")
os.system("pdfgrep 'net profit for the year' *.pdf")
os.system("pdfgrep 'Gross (loss) profit' *.pdf")
print("\n")
print("\n")

print("Total Equity")
os.system("pdfgrep 'stockholders equity' *.pdf")
os.system("pdfgrep 'shareholders equity' *.pdf")
os.system("pdfgrep 'net asset' *.pdf")
print("\n")
print("\n")

print("Currency of financial items")
os.system("pdfgrep -A1 -B1 'functional currency is' *.pdf")
print("\n")
print("\n")
