import {Component, Input, OnInit} from '@angular/core';
import {PodcastStatistics} from "../podcast";

@Component({
  selector: 'app-statistics-table',
  templateUrl: './statistics-table.component.html',
  styleUrls: ['./statistics-table.component.css']
})
export class StatisticsTableComponent implements OnInit {

  @Input() statistics: PodcastStatistics;

  constructor() {
  }

  ngOnInit() {
  }

}
