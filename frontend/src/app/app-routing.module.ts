import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {PodcastsComponent} from "./podcasts/podcasts.component";

const routes: Routes = [
  {path: '', redirectTo: '/podcasts', pathMatch: 'full'},
  {path: 'podcasts', component: PodcastsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
