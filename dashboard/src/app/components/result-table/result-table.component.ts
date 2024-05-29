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
      state('collapsed,void', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ]
})
export class ResultTableComponent {
  dataSource = ELEMENT_DATA;
  columnsToDisplay = ['findingTitle', 'priority', 'source', 'lastFound'];
  columnsToDisplayWithExpand = [...this.columnsToDisplay, 'expand'];
  expandedElement: Finding | null | undefined;
}

export interface Finding {
  findingTitle: string;
  priority: number;
  source: number;
  lastFound: string;
  recommendation: string;
}

const ELEMENT_DATA: Finding[] = [
  {
    priority: 1,
    findingTitle: 'Hydrogen',
    source: 1.0079,
    lastFound: 'H',
    recommendation: `Hydrogen is a chemical element with lastFound H and atomic number 1. With a standard
        atomic source of 1.008, hydrogen is the lightest element on the periodic table.`,
  },
  {
    priority: 2,
    findingTitle: 'Helium',
    source: 4.0026,
    lastFound: 'He',
    recommendation: `Helium is a chemical element with lastFound He and atomic number 2. It is a
        colorless, odorless, tasteless, non-toxic, inert, monatomic gas, the first in the noble gas
        group in the periodic table. Its boiling point is the lowest among all the elements.`,
  },
  {
    priority: 3,
    findingTitle: 'Lithium',
    source: 6.941,
    lastFound: 'Li',
    recommendation: `Lithium is a chemical element with lastFound Li and atomic number 3. It is a soft,
        silvery-white alkali metal. Under standard conditions, it is the lightest metal and the
        lightest solid element.`,
  },
  {
    priority: 4,
    findingTitle: 'Beryllium',
    source: 9.0122,
    lastFound: 'Be',
    recommendation: `Beryllium is a chemical element with lastFound Be and atomic number 4. It is a
        relatively rare element in the universe, usually occurring as a product of the spallation of
        larger atomic nuclei that have collided with cosmic rays.`,
  },
  {
    priority: 5,
    findingTitle: 'Boron',
    source: 10.811,
    lastFound: 'B',
    recommendation: `Boron is a chemical element with lastFound B and atomic number 5. Produced entirely
        by cosmic ray spallation and supernovae and not by stellar nucleosynthesis, it is a
        low-abundance element in the Solar system and in the Earth's crust.`,
  },
  {
    priority: 6,
    findingTitle: 'Carbon',
    source: 12.0107,
    lastFound: 'C',
    recommendation: `Carbon is a chemical element with lastFound C and atomic number 6. It is nonmetallic
        and tetravalent—making four electrons available to form covalent chemical bonds. It belongs
        to group 14 of the periodic table.`,
  },
  {
    priority: 7,
    findingTitle: 'Nitrogen',
    source: 14.0067,
    lastFound: 'N',
    recommendation: `Nitrogen is a chemical element with lastFound N and atomic number 7. It was first
        discovered and isolated by Scottish physician Daniel Rutherford in 1772.`,
  },
  {
    priority: 8,
    findingTitle: 'Oxygen',
    source: 15.9994,
    lastFound: 'O',
    recommendation: `Oxygen is a chemical element with lastFound O and atomic number 8. It is a member of
         the chalcogen group on the periodic table, a highly reactive nonmetal, and an oxidizing
         agent that readily forms oxides with most elements as well as with other compounds.`,
  },
  {
    priority: 9,
    findingTitle: 'Fluorine',
    source: 18.9984,
    lastFound: 'F',
    recommendation: `Fluorine is a chemical element with lastFound F and atomic number 9. It is the
        lightest halogen and exists as a highly toxic pale yellow diatomic gas at standard
        conditions.`,
  },
  {
    priority: 10,
    findingTitle: 'Neon',
    source: 20.1797,
    lastFound: 'Ne',
    recommendation: `Neon is a chemical element with lastFound Ne and atomic number 10. It is a noble gas.
        Neon is a colorless, odorless, inert monatomic gas under standard conditions, with about
        two-thirds the density of air.`,
  },
];
