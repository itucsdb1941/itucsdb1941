import { Component, OnInit } from '@angular/core';
import { Food } from '../../models/app.model';
import { AppService } from '../../services/app.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-new-password',
  templateUrl: './new-password.component.html',
  styleUrls: ['./new-password.component.css']
})
export class NewPasswordComponent implements OnInit {
	Username: string;
	Email: string;
	Answer: string;
	Ques: string;
	person: Array<any> = [];
	isCorrect: boolean = false;
	showAns: boolean = false;
	members: any[] = [];
	
  constructor(private route: ActivatedRoute, private appService: AppService, private router: Router) { 
	this.userLogin();
	
	}

	ngOnInit() {
  	}
  	sign(): void {
		this.person.push({
			'UserName': this.Username,
			'Email': this.Email,
			'Question': this.Ques

		});
		this.appService.postPerson(this.person);
	}

  	userLogin(): void {
		this.appService.getMembers().subscribe(member => this.members = member);
	}

  	login(): void{	
		this.router.navigateByUrl('/login-page');		
	}
	
	question(): void{
		this.members.forEach(row => {
			if(this.Username === row.username && this.Email === row.e_mail){
				this.Ques = row.recoveryQues;
				this.isCorrect = true;
			}
			else if(this.Answer === row.recoveryAns){
				this.router.navigateByUrl('/foods-list');	
				this.isCorrect = true;
			}
			
		})
	}
}
