import { Component, OnInit } from '@angular/core';
import { Food } from '../../models/app.model';
import { AppService } from '../../services/app.service';
import { ActivatedRoute, Router } from '@angular/router';
import { typeWithParameters } from '@angular/compiler/src/render3/util';

@Component({
  selector: 'food-menu',
  templateUrl: './food-menu.component.html',
  styleUrls: ['./food-menu.component.css']
})
export class FoodMenuComponent implements OnInit {

	foods: any[] = [];
	recipes: any[] = [];
	fName: string;
	foodID: Food[] = [];

	constructor(private route: ActivatedRoute, private appService: AppService, private router: Router) { 
		
	}
	
	ngOnInit() {
		
		this.getFood();
	}
	getFood(): void {
		this.appService.foodMenu().subscribe(food => this.foods = food);
	}
} 

