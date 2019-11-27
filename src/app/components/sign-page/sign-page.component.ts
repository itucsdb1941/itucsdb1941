import { Component, OnInit } from '@angular/core';
import { Food } from '../../models/app.model';
import { AppService } from '../../services/app.service';
import { ActivatedRoute, Router } from '@angular/router';

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

	constructor(private route: ActivatedRoute, private appService: AppService, private router: Router) { }

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
			'Location':this.Location,
			'Email': this.Email,
			'RecoveryQuestion': this.RecoveryQuestion,
			'RecoveryAnswer': this.RecoveryResult
		});
		this.appService.postPerson(this.person);
	}
	onGenderChange(event : any)
	{
		this.Gender = event.target.value;
	}
  
	login(): void{
		this.router.navigateByUrl('/login-page');
	}

}
