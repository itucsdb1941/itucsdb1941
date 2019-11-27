import { Component, OnInit } from '@angular/core';
import { Food } from '../../models/app.model';
import { AppService } from '../../services/app.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'dessert-menu',
  templateUrl: './dessert-menu.component.html',
  styleUrls: ['./dessert-menu.component.css']
})
export class DessertMenuComponent implements OnInit {

  	desserts: any[] = [];

	constructor(private route: ActivatedRoute, private appService: AppService, private router: Router) { 

	}
	
	
	ngOnInit() {
		this.getDesserts();
	}
	
	getDesserts(): void {
		this.appService.dessertMenu().subscribe(dessert => this.desserts= dessert);
		console.log(this.desserts);
	}
}
