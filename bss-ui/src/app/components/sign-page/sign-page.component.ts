import { Component, OnInit } from '@angular/core';
import { Food } from '../../models/app.model';
import { AppService } from '../../services/app.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'sign-page',
  templateUrl: './sign-page.component.html',
  styleUrls: ['./sign-page.component.css']
})
export class SignComponent implements OnInit {
	person: Array<any> = [];
	FirstName : string;
	LastName: string;
	Username: string;
	Password: string;
	Birthdate: string;
	Gender: string;
	Location:string;
	RecoveryQuestion: string;
	RecoveryResult: string;
	Email: string;
	ele: any;
	selected: string;

	constructor(private route: ActivatedRoute, private appService: AppService) { }

	ngOnInit() {
		console.log(this.selected)
	}

	
	sign(): void {
		this.person.push({
			'FirstName': this.FirstName,
			'LastName': this.LastName,
			'UserName': this.Username,
			'Password': this.Password,
			'Birthdate':this.Birthdate,
			'Gender':this.Gender,
			'Location':this.Location
		});
		this.appService.postPerson(this.person);
	}
	onGenderChange(event : any)
	{
		console.log(event.target.value);
	}
  

}
