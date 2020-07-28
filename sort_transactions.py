import sys
import re

# Usage:
# python sort_transactions.py finances.beancount >  finances.beancount.tmp
# bean-check finances.beancount.tmp
# mv finances.beancount.tmp finances.beancount

def get_date(tx):
  return tx[0][0:10]

f = open(sys.argv[1], "r")
postings = []
tx = ""
transactions = []
unknown_lines = []
skipped_lines = []
skip_lines = True
in_quote = False

for line in f.readlines():

  if re.match(r".*TRANSACTIONS", line):
    skipped_lines.append(line)
    skip_lines=False
    continue

  if skip_lines == True:
    skipped_lines.append(line)
    continue

  if in_quote:
    quotes = line.count('"')

    # quote ends when there is another odd number of quotes
    in_quote = quotes == 0 or 1 == ( quotes % 2 )

    postings.append(line)

  elif re.match(r"\d\d\d\d-\d\d-\d\d", line):
    if len(tx) > 0 :
      transactions.append((tx, postings))
    tx = line

    # quote starts if there's an odd number of quotes on the date line
    in_quote = 1 == ( line.count('"') % 2 )

    postings = []

  elif re.match(r"\s+\S.*\n", line):
    postings.append(line)

  elif re.match("\n", line):
    if(len(line) > 1) :
      # This is something weird and we need to handle it
      print(line, file=sys.stderr)
  else:
    unknown_lines.append(line)

# Dont forget to add the last transaction
if len(tx) > 0 :
  transactions.append((tx, postings))

# Print the header stuff
for line in skipped_lines:
  print(line, end = '')

# Sort and print all the remaining directives, separated by a newline
transactions.sort(key=get_date)
for [tx, postings] in transactions:
  print(tx, end ='')
  for posting in postings:
    print(posting, end = '')
  print()


# Print to stderr any messages that will be deleted
if len(unknown_lines)>0:
  print("Found %d Lines that dont match anything that will be deleted." % len(unknown_lines), file=sys.stderr)
  for line in unknown_lines:
    print(line, file = sys.stderr)
