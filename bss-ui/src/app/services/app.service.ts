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
  
  getMembers(): Observable<any[]> {
    return this.http.get<any[]>(this.userUrl + '/login-page');
  }
  getPassword(): Observable<any[]> {
    return this.http.get<any[]>(this.userUrl + '/new-password');
  }
  postPerson(data : any): any {
    return this.http.post<any[]>(this.userUrl + '/sign-register' , data , httpOptions ).subscribe(element => console.log(element));
  }
  foodMenu(): Observable<any[]> {
    return this.http.get<any[]>(this.userUrl + '/food-menu');
  }
  drinkMenu(): Observable<any[]> {
    return this.http.get<any[]>(this.userUrl + '/drink-menu');
  }
  dessertMenu(): Observable<any[]> {
    return this.http.get<any[]>(this.userUrl + '/dessert-menu');
  }
  recipePage(id: number, type: string): any {
    console.log(id);
    return this.http.get<any>(this.userUrl + '/recipe/'+ type +"/"+ id);
  }
  getComments(): Observable<any[]> {
    return this.http.get<any[]>(this.userUrl + '/foods-list');
  }





}