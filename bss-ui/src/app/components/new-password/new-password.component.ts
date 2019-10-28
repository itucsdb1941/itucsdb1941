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
	Password: string;
	Answer: string;
	memberId: any[] = [];
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
		this.router.navigateByUrl('/login-page');		
	}
	
}
