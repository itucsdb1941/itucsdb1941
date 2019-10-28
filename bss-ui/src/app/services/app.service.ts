import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Food } from '../models/app.model';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json'})
};

@Injectable({ providedIn: 'root' })
export class AppService {

  private userUrl = 'http://localhost:5000';  // URL to REST API

  constructor(private http: HttpClient) { 
    
  }

  /** GET users from the server */
  getFood(): Observable<Food[]> {
    return this.http.get<Food[]>(this.userUrl + '/foods-list');
  }
  getMembers(): Observable<any[]> {
    return this.http.get<any[]>(this.userUrl + '/login-page');
  }
  password(): Observable<any[]> {
    return this.http.get<any[]>(this.userUrl + '/new-password');
  }
  /** GET user by id. Will 404 if id not found */
  postPerson(data : any): any {
    return this.http.post<any[]>(this.userUrl + '/sign-register' , data , httpOptions ).subscribe(element => console.log(element));
  }
}