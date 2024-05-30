import { animate, state, style, transition, trigger } from '@angular/animations';
import { Component } from '@angular/core';

/**
 * @title Table with expandable rows
 */
@Component({
  selector: 'app-result-table',
  templateUrl: './result-table.component.html',
  styleUrls: ['./result-table.component.scss'],
  animations: [
    trigger('detailExpand', [
      state('collapsed,void', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition(
        'expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')
      ),
    ]),
  ],
})
export class ResultTableComponent {
  dataSource = ELEMENT_DATA;
  columnsToDisplay = ['findingTitle', 'priority', 'source', 'lastFound'];
  columnsToDisplayWithExpand = [...this.columnsToDisplay, 'expand'];
  expandedElement: Finding | null | undefined;

  public formatColumn(col: string): string {
    return col
      .replace(/([a-z])([A-Z])/g, '$1 $2') // Insert space before capital letters
      .split(' ') // Split the string into words
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize the first letter of each word
      .join(' ');
  }
}

export interface Finding {
  findingTitle: string;
  description: string;
  priority: number;
  source: string;
  lastFound: string;
  recommendation: string;
}

const ELEMENT_DATA: Finding[] = [
  {
    priority: 1,
    findingTitle: 'use-after-free caused by do_submit_urb()',
    description:
      'A use-after-free vulnerability was found in the siano smsusb module in the Linux kernel. The bug occurs during device initialization when the siano device is plugged in. This flaw allows a local user to crash the system, causing a denial of service condition.',
    source: 'Trivy',
    lastFound: '2023-08-25T15:48:01+00:00',
    recommendation: `Hydrogen is a chemical element with lastFound H and atomic number 1. With a standard
        atomic source of 1.008, hydrogen is the lightest element on the periodic table.`,
  },
  {
    priority: 2,
    findingTitle:
      'tar: does not properly warn the user when extracting setuid or setgid files',
    description:
      'Tar 1.15.1 does not properly warn the user when extracting setuid or setgid files, which may allow local users or remote attackers to gain privileges.',
    source: 'Trivy',
    lastFound: '2024-02-21T12:50:08+00:00',
    recommendation: `Helium is a chemical element with lastFound He and atomic number 2. It is a
        colorless, odorless, tasteless, non-toxic, inert, monatomic gas, the first in the noble gas
        group in the periodic table. Its boiling point is the lowest among all the elements.`,
  },
  {
    priority: 3,
    findingTitle:
      'libtiff: out-of-bounds read in extractContigSamplesShifted8bits() in tools/tiffcrop.c',
    description:
      'LibTIFF 4.4.0 has an out-of-bounds read in tiffcrop in tools/tiffcrop.c:3400, allowing attackers to cause a denial-of-service via a crafted tiff file. For users that compile libtiff from sources, the fix is available with commit afaabc3e.',
    source: 'Trivy',
    lastFound: '2023-03-28T15:48:42+00:00',
    recommendation: `Lithium is a chemical element with lastFound Li and atomic number 3. It is a soft,
        silvery-white alkali metal. Under standard conditions, it is the lightest metal and the
        lightest solid element.`,
  },
];
