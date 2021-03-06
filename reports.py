#
# A new home for the reporting code.
#
# This code is part of the LWN git data miner.
#
# Copyright 2007-11 Eklektix, Inc.
# Copyright 2007-11 Jonathan Corbet <corbet@lwn.net>
#
# This file may be distributed under the terms of the GNU General
# Public License, version 2.
#

import sys

Outfile = sys.stdout
HTMLfile = None
ListCount = 999999


def SetOutput (file):
    global Outfile
    Outfile = file

def SetHTMLOutput (file):
    global HTMLfile
    HTMLfile = file

def SetMaxList (max):
    global ListCount
    ListCount = max


def Write (stuff):
    Outfile.write (stuff)



#
# HTML output support stuff.
#
HTMLclass = 0
HClasses = ['Even', 'Odd']

THead = '''<p>
<table cellspacing=3>
<tr><th colspan=3>%s</th></tr>
'''

def BeginReport (title):
    global HTMLclass
    
    Outfile.write ('\n%s\n' % title)
    if HTMLfile:
        HTMLfile.write (THead % title)
        HTMLclass = 0

TRow = '''    <tr class="%s">
<td>%s</td><td align="right">%d</td><td align="right">%.1f%%</td></tr>
'''

def ReportLine (text, count, pct):
    global HTMLclass
    if count == 0:
        return
    Outfile.write ('%-25s %4d (%.1f%%)\n' % (text, count, pct))
    if HTMLfile:
        HTMLfile.write (TRow % (HClasses[HTMLclass], text, count, pct))
        HTMLclass ^= 1

def EndReport (text=None):
    if text:
        Outfile.write ('%s\n' % (text, ))
    if HTMLfile:
        HTMLfile.write ('</table>\n\n')
        
#
# Comparison and report generation functions.
#
def ComparePCount (h1, h2):
    return len (h2.patches) - len (h1.patches)

def ReportByPCount (hlist, cscount):
    hlist.sort (ComparePCount)
    count = reported = 0
    BeginReport ('Developers with the most changesets')
    for h in hlist:
        pcount = len (h.patches)
        changed = max(h.added, h.removed)
        delta = h.added - h.removed
        if pcount > 0:
            ReportLine (h.name, pcount, (pcount*100.0)/cscount)
            reported += pcount
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of changesets' % ((reported*100.0)/cscount, ))

def CompareBCount (h1, h2):
    return len (h2.bugsfixed) - len (h1.bugsfixed)

def ReportByBCount (hlist, totalbugs):
    hlist.sort (CompareBCount)
    count = reported = 0
    BeginReport ('Developers with the most bugs fixed')
    for h in hlist:
        bcount = len (h.bugsfixed)
        if bcount > 0:
            ReportLine (h.name, bcount, (bcount*100.0)/totalbugs)
            reported += bcount
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of bugs' % ((reported*100.0)/totalbugs, ))

def CompareLChanged (h1, h2):
    return max(h2.added, h2.removed) - max(h1.added, h1.removed)

def ReportByLChanged (hlist, totalchanged):
    hlist.sort (CompareLChanged)
    count = reported = 0
    BeginReport ('Developers with the most changed lines')
    for h in hlist:
        pcount = len (h.patches)
        changed = max(h.added, h.removed)
        delta = h.added - h.removed
        if (h.added + h.removed) > 0:
            ReportLine (h.name, changed, (changed*100.0)/totalchanged)
            reported += changed
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of changes' % ((reported*100.0)/totalchanged, ))
            
def CompareLRemoved (h1, h2):
    return (h2.removed - h2.added) - (h1.removed - h1.added)

def ReportByLRemoved (hlist, totalremoved):
    hlist.sort (CompareLRemoved)
    count = reported = 0
    BeginReport ('Developers with the most lines removed')
    for h in hlist:
        pcount = len (h.patches)
        changed = max(h.added, h.removed)
        delta = h.added - h.removed
        if delta < 0:
            ReportLine (h.name, -delta, (-delta*100.0)/totalremoved)
            reported += -delta
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of changes' % ((reported*100.0)/totalremoved, ))

def CompareEPCount (e1, e2):
    return e2.count - e1.count

def ReportByPCEmpl (elist, cscount):
    elist.sort (CompareEPCount)
    count = total_pcount = 0
    BeginReport ('Top changeset contributors by employer')
    for e in elist:
        if e.count != 0:
            ReportLine (e.name, e.count, (e.count*100.0)/cscount)
            total_pcount += e.count
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of changesets' % ((total_pcount*100.0)/cscount, ))

def CompareEBCount (e1, e2):
    return len (e2.bugsfixed) - len (e1.bugsfixed)

def ReportByBCEmpl (elist, totalbugs):
    elist.sort (CompareEBCount)
    count = reported = 0
    BeginReport ('Top bugs fixed by employer')
    for e in elist:
        if len(e.bugsfixed) != 0:
            ReportLine (e.name, len(e.bugsfixed), (len(e.bugsfixed)*100.0)/totalbugs)
            reported += len(e.bugsfixed)
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of bugs' % ((reported*100.0)/totalbugs, ))

def CompareELChanged (e1, e2):
    return e2.changed - e1.changed

def ReportByELChanged (elist, totalchanged):
    elist.sort (CompareELChanged)
    count = reported = 0
    BeginReport ('Top lines changed by employer')
    for e in elist:
        if e.changed != 0:
            ReportLine (e.name, e.changed, (e.changed*100.0)/totalchanged)
            reported += e.changed
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of changes' % ((reported*100.0)/totalchanged, ))



def CompareSOBs (h1, h2):
    return len (h2.signoffs) - len (h1.signoffs)

def ReportBySOBs (hlist):
    hlist.sort (CompareSOBs)
    totalsobs = 0
    for h in hlist:
        totalsobs += len (h.signoffs)
    count = reported = 0
    BeginReport ('Developers with the most signoffs (total %d)' % totalsobs)
    for h in hlist:
        scount = len (h.signoffs)
        if scount > 0:
            ReportLine (h.name, scount, (scount*100.0)/totalsobs)
            reported += scount
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of signoffs' % ((reported*100.0)/totalsobs, ))

#
# Reviewer reporting.
#
def CompareRevs (h1, h2):
    return len (h2.reviews) - len (h1.reviews)

def ReportByRevs (hlist):
    hlist.sort (CompareRevs)
    totalrevs = 0
    for h in hlist:
        totalrevs += len (h.reviews)
    count = reported = 0
    BeginReport ('Developers with the most reviews (total %d)' % totalrevs)
    for h in hlist:
        scount = len (h.reviews)
        if scount > 0:
            ReportLine (h.name, scount, (scount*100.0)/totalrevs)
            reported += scount
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of reviews' % ((reported*100.0)/totalrevs, ))

def CompareRevsEmpl (e1, e2):
    return len (e2.reviews) - len (e1.reviews)

def ReportByRevsEmpl (elist):
    elist.sort (CompareRevsEmpl)
    totalrevs = 0
    for e in elist:
        totalrevs += len (e.reviews)
    count = reported = 0
    BeginReport ('Top reviewers by employer (total %d)' % totalrevs)
    for e in elist:
        scount = len (e.reviews)
        if scount > 0:
            ReportLine (e.name, scount, (scount*100.0)/totalrevs)
            reported += scount
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of reviews' % ((reported*100.0)/totalrevs, ))

#
# tester reporting.
#
def CompareTests (h1, h2):
    return len (h2.tested) - len (h1.tested)

def ReportByTests (hlist):
    hlist.sort (CompareTests)
    totaltests = 0
    for h in hlist:
        totaltests += len (h.tested)
    count = reported = 0
    BeginReport ('Developers with the most test credits (total %d)' % totaltests)
    for h in hlist:
        scount = len (h.tested)
        if scount > 0:
            ReportLine (h.name, scount, (scount*100.0)/totaltests)
            reported += scount
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of test credits' % ((reported*100.0)/totaltests, ))

def CompareTestCred (h1, h2):
    return h2.testcred - h1.testcred

def ReportByTestCreds (hlist):
    hlist.sort (CompareTestCred)
    totaltests = 0
    for h in hlist:
        totaltests += h.testcred
    count = reported = 0
    BeginReport ('Developers who gave the most tested-by credits (total %d)' % totaltests)
    for h in hlist:
        if h.testcred > 0:
            ReportLine (h.name, h.testcred, (h.testcred*100.0)/totaltests)
            reported += h.testcred
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of test credits' % ((reported*100.0)/totaltests, ))



#
# Reporter reporting.
#
def CompareReports (h1, h2):
    return len (h2.reports) - len (h1.reports)

def ReportByReports (hlist):
    hlist.sort (CompareReports)
    totalreps = 0
    for h in hlist:
        totalreps += len (h.reports)
    count = reported = 0
    BeginReport ('Developers with the most report credits (total %d)' % totalreps)
    for h in hlist:
        scount = len (h.reports)
        if scount > 0:
            ReportLine (h.name, scount, (scount*100.0)/totalreps)
            report += scount
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of report credits' % ((reported*100.0)/totalreps, ))

def CompareRepCred (h1, h2):
    return h2.repcred - h1.repcred

def ReportByRepCreds (hlist):
    hlist.sort (CompareRepCred)
    totalreps = 0
    for h in hlist:
        totalreps += h.repcred
    count = reported = 0
    BeginReport ('Developers who gave the most report credits (total %d)' % totalreps)
    for h in hlist:
        if h.repcred > 0:
            ReportLine (h.name, h.repcred, (h.repcred*100.0)/totalreps)
            reported += h.repcred
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of report credits' % ((reported*100.0)/totalreps, ))



def CompareESOBs (e1, e2):
    return e2.sobs - e1.sobs

def ReportByESOBs (elist):
    elist.sort (CompareESOBs)
    totalsobs = 0
    for e in elist:
        totalsobs += e.sobs
    count = reported = 0
    BeginReport ('Employers with the most signoffs (total %d)' % totalsobs)
    for e in elist:
        if e.sobs > 0:
            ReportLine (e.name, e.sobs, (e.sobs*100.0)/totalsobs)
            reported += e.sobs
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of signoffs' % ((reported*100.0)/totalsobs, ))
   
def CompareHackers (e1, e2):
    return len (e2.hackers) - len (e1.hackers)

def ReportByEHackers (elist):
    elist.sort (CompareHackers)
    totalhackers = 0
    for e in elist:
        totalhackers += len (e.hackers)
    count = reported = 0
    BeginReport ('Employers with the most hackers (total %d)' % totalhackers)
    for e in elist:
        nhackers = len (e.hackers)
        if nhackers > 0:
            ReportLine (e.name, nhackers, (nhackers*100.0)/totalhackers)
            reported += nhackers
        count += 1
        if count >= ListCount:
            break
    EndReport ('Covers %f%% of hackers' % ((reported*100.0)/totalhackers, ))


def DevReports (hlist, totalchanged, cscount, totalremoved):
    ReportByPCount (hlist, cscount)
    ReportByLChanged (hlist, totalchanged)
    ReportByLRemoved (hlist, totalremoved)
    #ReportBySOBs (hlist)
    #ReportByRevs (hlist)
    #ReportByTests (hlist)
    #ReportByTestCreds (hlist)
    #ReportByReports (hlist)
    #ReportByRepCreds (hlist)

def EmplReports (elist, totalchanged, cscount):
    ReportByPCEmpl (elist, cscount)
    ReportByELChanged (elist, totalchanged)
    #ReportByESOBs (elist)
    ReportByEHackers (elist)

def DevBugReports (hlist, totalbugs):
    ReportByBCount (hlist, totalbugs)

def EmplBugReports (elist, totalbugs):
    ReportByBCEmpl (elist, totalbugs)

def DevReviews (hlist, totalreviews):
    ReportByRevs (hlist)

def EmplReviews (elist, totalreviews):
    ReportByRevsEmpl (elist)

def ReportByFileType (hacker_list):
    total = {}
    total_by_hacker = {}

    BeginReport ('Developer contributions by type')
    for h in hacker_list:
        by_hacker = {}
        for patch in h.patches:
            # Get a summary by hacker
            for (filetype, (added, removed)) in patch.filetypes.iteritems():
                if by_hacker.has_key(filetype):
                    by_hacker[filetype][patch.ADDED] += added
                    by_hacker[filetype][patch.REMOVED] += removed
                else:
                    by_hacker[filetype] = [added, removed]

                # Update the totals
                if total.has_key(filetype):
                    total[filetype][patch.ADDED] += added
                    total[filetype][patch.REMOVED] += removed
                else:
                    total[filetype] = [added, removed, []]

        # Print a summary by hacker
        print h.name
        for filetype, counters in by_hacker.iteritems():
            print '\t', filetype, counters
            h_added = by_hacker[filetype][patch.ADDED]
            h_removed = by_hacker[filetype][patch.REMOVED]
            total[filetype][2].append ([h.name, h_added, h_removed])

    # Print the global summary
    BeginReport ('Contributions by type and developers')
    for filetype, (added, removed, hackers) in total.iteritems():
        print filetype, added, removed
        for h, h_added, h_removed in hackers:
            print '\t%s: [%d, %d]' % (h, h_added, h_removed)

    # Print the very global summary
    BeginReport ('General contributions by type')
    for filetype, (added, removed, hackers) in total.iteritems():
        print filetype, added, removed
