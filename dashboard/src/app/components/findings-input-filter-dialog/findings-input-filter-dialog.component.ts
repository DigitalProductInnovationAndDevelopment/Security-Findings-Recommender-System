import { ChangeDetectorRef, Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
export interface Task {
  name: string;
  completed: boolean;
  subtasks?: Task[];
}

@Component({
  selector: 'app-findings-input-filter-dialog',
  templateUrl: './findings-input-filter-dialog.component.html',
  styleUrl: './findings-input-filter-dialog.component.scss',
})
export class FindingsInputFilterDialogComponent {
  filterForm: FormGroup = new FormGroup({
    sources: new FormControl([]),
    cve_ids: new FormControl([]),
    cwe_ids: new FormControl([]),
    sourcesInput: new FormControl(''),
    cve_idsInput: new FormControl(''),
    cwe_idsInput: new FormControl(''),
  });
  filterNames = ['severities', 'priorities', 'sources', 'cve_ids', 'cwe_ids'];

  task: Task = {
    name: 'Select all Findings',
    completed: true,
    subtasks: [
      { name: 'Severities', completed: true },
      { name: 'Priorities', completed: true },
      { name: 'CVE_IDs', completed: true },
      { name: 'CWE_IDs', completed: true },
      { name: 'Sources', completed: true },
    ],
  };

  rangeFilters = {
    severities: { minValue: 0, maxValue: 100 },
    priorities: { minValue: 0, maxValue: 100 },
  };

  constructor(
    public dialogRef: MatDialogRef<FindingsInputFilterDialogComponent>,
    private cdr: ChangeDetectorRef
  ) {}

  closeDialog(): void {
    const source = this.filterForm.get('sources')?.value;
    const cve_ids = this.filterForm.get('cve_ids')?.value;
    const cwe_ids = this.filterForm.get('cwe_ids')?.value;
    const sevMinValue = this.rangeFilters.severities.minValue;
    const sevMaxValue = this.rangeFilters.severities.maxValue;
    const priMinValue = this.rangeFilters.priorities.minValue;
    const priMaxValue = this.rangeFilters.priorities.maxValue;
    this.dialogRef.close({
      ...((sevMinValue !== 0 || sevMaxValue !== 100) && {
        severity: [
          this.rangeFilters.severities.minValue,
          this.rangeFilters.severities.maxValue,
        ],
      }),
      ...((priMinValue !== 0 || priMaxValue !== 100) && {
        priority: [
          this.rangeFilters.priorities.minValue,
          this.rangeFilters.priorities.maxValue,
        ],
      }),
      ...(source && source.length > 0 && { source }),
      ...(cve_ids && cve_ids.length > 0 && { cve_ids }),
      ...(cwe_ids && cwe_ids.length > 0 && { cwe_ids }),
    });
  }

  allComplete: boolean = true;

  updateAllComplete() {
    this.allComplete =
      this.task.subtasks != null &&
      this.task.subtasks.every((t) => t.completed);
  }

  someComplete(): boolean {
    if (this.task.subtasks == null) {
      return false;
    }
    return (
      this.task.subtasks.filter((t) => t.completed).length > 0 &&
      !this.allComplete
    );
  }

  setAll(completed: boolean) {
    this.allComplete = completed;
    if (this.task.subtasks == null) {
      return;
    }
    this.task.subtasks.forEach((t) => (t.completed = completed));
  }
  addCve(): void {
    const cve_idsInput = this.filterForm.get('cve_idsInput');
    const cve_ids = this.filterForm.get('cve_ids')?.value;

    if (cve_idsInput?.value && cve_idsInput.value.trim() !== '') {
      cve_ids.push(cve_idsInput.value.trim());
      this.filterForm.patchValue({ cve_ids: cve_ids });
      cve_idsInput.setValue('');
    }
  }

  addCwe(): void {
    const cwe_idsInput = this.filterForm.get('cwe_idsInput');
    const cwe_ids = this.filterForm.get('cwe_ids')?.value;

    if (cwe_idsInput?.value && cwe_idsInput.value.trim() !== '') {
      cwe_ids.push(cwe_idsInput.value.trim());
      this.filterForm.patchValue({ cwe_ids: cwe_ids });
      cwe_idsInput.setValue('');
    }
  }

  addSource(): void {
    const sourcesInput = this.filterForm.get('sourcesInput');
    const sources = this.filterForm.get('sources')?.value;

    if (sourcesInput?.value && sourcesInput.value.trim() !== '') {
      sources.push(sourcesInput.value.trim());
      this.filterForm.patchValue({ sources: sources });
      sourcesInput.setValue('');
    }
  }

  removeSource(value: string): void {
    const sources = this.filterForm.get('sources')?.value;

    if (sources) {
      const index = sources.indexOf(value);
      if (index >= 0) {
        sources.splice(index, 1);
        this.filterForm.patchValue({ sources: sources });
      }
    }
  }

  removeCve(value: string): void {
    const cve_ids = this.filterForm.get('cve_ids')?.value;

    if (cve_ids) {
      const index = cve_ids.indexOf(value);
      if (index >= 0) {
        cve_ids.splice(index, 1);
        this.filterForm.patchValue({ cve_ids: cve_ids });
      }
    }
  }

  removeCwe(value: string): void {
    const cwe_ids = this.filterForm.get('cwe_ids')?.value;

    if (cwe_ids) {
      const index = cwe_ids.indexOf(value);
      if (index >= 0) {
        cwe_ids.splice(index, 1);
        this.filterForm.patchValue({ cwe_ids: cwe_ids });
      }
    }
  }
}
