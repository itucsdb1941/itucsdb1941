import { Component, OnInit } from '@angular/core';
import { Food } from '../../models/app.model';
import { AppService } from '../../services/app.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'food-list',
  templateUrl: './food-list.component.html',
  styleUrls: ['./food-list.component.css']
})
export class FoodListComponent implements OnInit {

  	comments: Food[] = [];

	constructor(private route: ActivatedRoute, private appService: AppService, private router: Router) { 

	}
	
	ngOnInit() {
		this.getComment();
	}
	foodMenu(): void{	
		this.router.navigateByUrl('/food-menu');		
	}
	drinkMenu(): void{	
		this.router.navigateByUrl('/drink-menu');		
	}
	dessertMenu(): void{	
		this.router.navigateByUrl('/dessert-menu');		
	}
    getComment(): void {
        this.appService.getComments().subscribe(comment => this.comments = comment);
        console.log(this.comments);
    }
}
