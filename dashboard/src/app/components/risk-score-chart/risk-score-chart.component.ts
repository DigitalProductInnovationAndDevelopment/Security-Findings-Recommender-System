import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-risk-score-chart',
  templateUrl: './risk-score-chart.component.html',
  styleUrl: './risk-score-chart.component.scss',
})
export class RiskScoreChartComponent implements OnInit {
  @Input() score: number = 30;
  ngOnInit(): void {
    const innerCircle = document.getElementById('inner-circle');
    innerCircle &&
      (innerCircle.style.transform = `rotate(${this.score * 3}deg)`);
  }
}
