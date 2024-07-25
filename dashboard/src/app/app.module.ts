import { NgModule } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { BrowserModule } from '@angular/platform-browser';

import { HttpClientModule } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatPaginatorModule } from '@angular/material/paginator';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgxsModule } from '@ngxs/store';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FindingsInputComponent } from './components/findings-input/findings-input.component';
import { FooterComponent } from './components/footer/footer.component';
import { HeaderComponent } from './components/header/header.component';
import { ResultTableComponent } from './components/result-table/result-table.component';
import { OverviewComponent } from './pages/overview/overview.component';
import { ResultsComponent } from './pages/results/results.component';
import { RecommendationsState } from './states/recommendations.state';

import { CommonModule, JsonPipe } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSliderModule } from '@angular/material/slider';
import { AggregatedSolutionsDialogComponent } from './components/aggregated-solutions-dialog/aggregated-solutions-dialog.component';
import { FindingDetailsDialogComponent } from './components/finding-details-dialog/finding-details-dialog.component';
import { FindingsInputFilterDialogComponent } from './components/findings-input-filter-dialog/findings-input-filter-dialog.component';
import { LoadingSpinnerComponent } from './components/loading-spinner/loading-spinner.component';
import { ResultAggregatedSolutionsCardsComponent } from './components/result-aggregated-solutions-cards/result-aggregated-solutions-cards.component';
import { RiskScoreChartComponent } from './components/risk-score-chart/risk-score-chart.component';

export const MaterialModules = [
  MatButtonModule,
  MatPaginatorModule,
  MatDialogModule,
  MatProgressSpinnerModule,
  MatCheckboxModule,
  MatFormFieldModule,
  MatInputModule,
  MatButtonModule,
  MatSliderModule,
  MatTableModule,
];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    OverviewComponent,
    ResultsComponent,
    FindingsInputComponent,
    ResultTableComponent,
    FindingDetailsDialogComponent,
    RiskScoreChartComponent,
    LoadingSpinnerComponent,
    FindingsInputFilterDialogComponent,
    ResultAggregatedSolutionsCardsComponent,
    AggregatedSolutionsDialogComponent,
  ],
  imports: [
    CommonModule,
    BrowserModule,
    AppRoutingModule,
    NgxsModule.forRoot([RecommendationsState]),
    HttpClientModule,
    MaterialModules,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    JsonPipe,
  ],
  exports: [CommonModule, MaterialModules],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
