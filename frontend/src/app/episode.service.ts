import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {Observable} from "rxjs";
import {API_URL} from "./env";
import {catchError} from "rxjs/operators";
import {Episode} from "./episode";

@Injectable({
  providedIn: 'root'
})
export class EpisodeService {

  constructor(private http: HttpClient) { }

  private static _handleError(err: HttpErrorResponse | any) {
    console.log(err);
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  getAllEpisodes(): Observable<Episode[]> {
    return this.http
      .get<Episode[]>(`${API_URL}/episodes`)
      .pipe(catchError(EpisodeService._handleError));
  }

}
