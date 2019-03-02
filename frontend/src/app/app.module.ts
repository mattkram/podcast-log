import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PodcastsComponent } from './podcasts/podcasts.component';
import { EpisodesComponent } from './episodes/episodes.component';
import {HttpClientModule} from "@angular/common/http";
import { PodcastDetailComponent } from './podcast-detail/podcast-detail.component';
import { StatisticsTableComponent } from './statistics-table/statistics-table.component';

@NgModule({
  declarations: [
    AppComponent,
    PodcastsComponent,
    EpisodesComponent,
    PodcastDetailComponent,
    StatisticsTableComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
