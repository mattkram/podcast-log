import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {PodcastsComponent} from "./podcasts/podcasts.component";
import {EpisodesComponent} from "./episodes/episodes.component";
import {PodcastDetailComponent} from "./podcast-detail/podcast-detail.component";

const routes: Routes = [
  {path: '', redirectTo: '/podcasts', pathMatch: 'full'},
  {path: 'podcasts', component: PodcastsComponent},
  {path: 'podcast/:id', component: PodcastDetailComponent},
  {path: 'episodes', component: EpisodesComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
