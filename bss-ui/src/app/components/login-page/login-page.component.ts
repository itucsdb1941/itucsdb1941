import { Component, OnInit } from '@angular/core';
import { Food } from '../../models/app.model';
import { AppService } from '../../services/app.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent implements OnInit {
	Username: string;
	Password: string;
	Answer: string;
	memberId: any[] = [];
	isCorrect: boolean = false;
	members: any[] = [];

	constructor(private route: ActivatedRoute, private appService: AppService, private router: Router) { 
		this.userLogin();
	}

	ngOnInit() {
		
	}

	userLogin(): void {
		this.appService.getMembers().subscribe(member => this.members = member);
		
	}
	login(): void{
		console.log(this.members)
		this.members.forEach(row => {
			if(row.username === this.Username && row.userPassword === this.Password)
			{
				this.router.navigateByUrl('/foods-list');
			}
			else
			{
				this.isCorrect = true;
			}
		})
	}

	password(): void{
		this.members.forEach(row => {
			this.router.navigateByUrl('/new-password');
		})
	}
	


}
