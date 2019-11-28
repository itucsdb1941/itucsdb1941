import { environment} from './environment';
import { HttpClient } from '@angular/common/http';
import {Injectable} from '@angular/core';

@Injectable()
export class DataService {
	 
	 baseUrl = environment.api;
	 constructor(private httpClient: HttpClient){}
	 getUser(id : number){
		 let url = this.baseUrl;
		 return this.httpClient.get<JSON>(url);
	 }
	
}